from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import escape
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

from walczak.display import (
    description_is_thin,
    key_differences,
    load_profile,
    paired_groups,
    profile_groups,
    split_profile,
)
from walczak.humor import choose_archetypes
from walczak.models import Archetype, Fact, HumorQuestion, IPIPItem, PreferenceQuestion, Study, Style, Tag
from walczak.preference import answers_complete, rank_styles
from walczak.psychology import score_ipip

RESULT_KEY = "walczak_result"
PREFERENCE_KEY = "walczak_preference"
IPIP_KEY = "walczak_ipip"
FACT_KEY = "walczak_facts"


def family_options() -> list[dict[str, str]]:
    return [
        {"value": value, "pl": label, "en": Style.FAMILY_EN[value]}
        for value, label in Style.FAMILY_CHOICES
    ]


@require_http_methods(["GET"])
def home(request: HttpRequest) -> HttpResponse:
    return render(request, "walczak/home.html")


@require_http_methods(["GET"])
def style_list(request: HttpRequest) -> HttpResponse:
    raw = request.GET.get("rodzina") or ""
    known = {value for value, _label in Style.FAMILY_CHOICES}
    selected = raw if raw in known else ""
    tag_raw = request.GET.get("tag") or ""
    tags = list(Tag.objects.all())
    known_tags = {tag.slug for tag in tags}
    selected_tag = tag_raw if tag_raw in known_tags else ""
    styles = Style.objects.filter(active=True)
    if selected:
        styles = styles.filter(family=selected)
    if selected_tag:
        styles = styles.filter(tags__slug=selected_tag).distinct()
    return render(
        request,
        "walczak/list.html",
        {
            "styles": styles,
            "families": family_options(),
            "tags": tags,
            "selected_family": selected,
            "selected_tag": selected_tag,
        },
    )


@require_http_methods(["GET"])
def style_detail(request: HttpRequest, slug: str) -> HttpResponse:
    style = get_object_or_404(
        Style.objects.prefetch_related(
            "sources",
            "style_types",
            "tags",
            "facts__sources",
            "relations_out__to_style",
            "relations_out__sources",
        ),
        slug=slug,
        active=True,
    )
    relations = [item for item in style.relations_out.all() if item.sources.all()]
    profile = load_profile(style)
    headline, rest = split_profile(profile)
    return render(
        request,
        "walczak/detail.html",
        {
            "style": style,
            "relations": relations,
            "headline": headline,
            "rest": rest,
            "thin_sources": description_is_thin(style),
        },
    )


@require_http_methods(["GET", "POST"])
@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def quiz(request: HttpRequest) -> HttpResponse:
    questions = list(
        HumorQuestion.objects.filter(active=True).prefetch_related("choices").order_by("sort_order", "pk")
    )
    if not questions:
        return render(request, "walczak/empty.html")
    if request.method == "POST":
        archetypes = choose_archetypes(questions, request.POST)
        if not archetypes:
            _forget(request, RESULT_KEY)
            return render(
                request,
                "walczak/quiz.html",
                {"questions": questions, "total": len(questions), "error": True},
            )
        request.session[RESULT_KEY] = {"archetype_slugs": [item.slug for item in archetypes]}
        return redirect("walczak:result")
    return render(request, "walczak/quiz.html", {"questions": questions, "total": len(questions)})


@require_http_methods(["GET"])
def result(request: HttpRequest) -> HttpResponse:
    payload = request.session.get(RESULT_KEY)
    slugs = payload.get("archetype_slugs") if isinstance(payload, dict) else None
    if not isinstance(slugs, list) or not all(isinstance(item, str) and item for item in slugs):
        return redirect("walczak:quiz")
    found = {
        item.slug: item
        for item in Archetype.objects.filter(slug__in=slugs).prefetch_related("styles")
    }
    archetypes = [found[slug] for slug in slugs if slug in found]
    if not archetypes:
        return redirect("walczak:quiz")
    cards = [
        {
            "archetype": archetype,
            "styles": list(archetype.styles.filter(active=True).order_by("slug")[:3]),
        }
        for archetype in archetypes
    ]
    return render(
        request,
        "walczak/result.html",
        {"cards": cards, "tied": len(cards) > 1},
    )


@require_http_methods(["GET", "POST"])
@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def preference_test(request: HttpRequest) -> HttpResponse:
    questions = list(
        PreferenceQuestion.objects.filter(active=True)
        .prefetch_related("options__weights")
        .order_by("sort_order", "pk")
    )
    if not questions:
        return render(request, "walczak/empty.html")
    if request.method == "POST":
        if not answers_complete(questions, request.POST):
            _forget(request, PREFERENCE_KEY)
            return render(
                request,
                "walczak/test.html",
                {"questions": questions, "total": len(questions), "error": True},
            )
        ranking = rank_styles(questions, request.POST)
        picks = ranking["picks"]
        if not picks:
            _forget(request, PREFERENCE_KEY)
            return render(
                request,
                "walczak/test.html",
                {"questions": questions, "total": len(questions), "error": True},
            )
        request.session[PREFERENCE_KEY] = {"picks": [_stored(row) for row in picks]}
        return redirect("walczak:match")
    return render(request, "walczak/test.html", {"questions": questions, "total": len(questions)})


@require_http_methods(["GET"])
def preference_result(request: HttpRequest) -> HttpResponse:
    payload = request.session.get(PREFERENCE_KEY)
    if not isinstance(payload, dict):
        return redirect("walczak:test")
    rows = _hydrate(payload.get("picks"))
    if not rows:
        return redirect("walczak:test")
    return render(request, "walczak/match.html", {"rows": rows})


@require_http_methods(["GET", "POST"])
@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def personality(request: HttpRequest) -> HttpResponse:
    items = list(IPIPItem.objects.select_related("scale").order_by("sort_order", "pk"))
    if request.method == "POST" and items:
        answers: dict[int, int] = {}
        for item in items:
            raw = request.POST.get(f"i{item.pk}")
            value: int | None = None
            if isinstance(raw, str):
                try:
                    parsed = int(raw)
                except ValueError:
                    parsed = None
                if parsed is not None and 1 <= parsed <= 5:
                    value = parsed
            if value is None:
                _forget(request, IPIP_KEY)
                return render(
                    request,
                    "walczak/personality.html",
                    {
                        "items": items,
                        "scores": None,
                        "error": True,
                        "attribution": items[0].attribution if items else "",
                    },
                )
            answers[item.pk] = value
        request.session[IPIP_KEY] = score_ipip(items, answers)
        return redirect("walczak:personality")
    payload = request.session.get(IPIP_KEY)
    shown: dict[str, float] | None = None
    if isinstance(payload, dict):
        shown = {str(key): float(value) for key, value in payload.items()}
    return render(
        request,
        "walczak/personality.html",
        {"items": items, "scores": shown, "attribution": items[0].attribution if items else ""},
    )


@require_http_methods(["GET", "POST"])
def compare_form(request: HttpRequest) -> HttpResponse:
    styles = Style.objects.filter(active=True, catalog_set="core").order_by("name_pl")
    if request.method == "POST":
        left = request.POST.get("a") or ""
        right = request.POST.get("b") or ""
        known = set(styles.values_list("slug", flat=True))
        if left == right or left not in known or right not in known:
            return render(request, "walczak/compare_form.html", {"styles": styles, "error": True})
        return redirect("walczak:compare", a=left, b=right)
    return render(request, "walczak/compare_form.html", {"styles": styles})


@require_http_methods(["GET"])
def compare(request: HttpRequest, a: str, b: str) -> HttpResponse:
    if a == b:
        styles = Style.objects.filter(active=True, catalog_set="core").order_by("name_pl")
        return render(request, "walczak/compare_form.html", {"styles": styles, "error": True})
    left = get_object_or_404(Style.objects.prefetch_related("style_types"), slug=a, active=True, catalog_set="core")
    right = get_object_or_404(Style.objects.prefetch_related("style_types"), slug=b, active=True, catalog_set="core")
    left_profile = load_profile(left)
    right_profile = load_profile(right)
    studies = (
        Study.objects.filter(styles__in=[left, right], sources__isnull=False)
        .distinct()
        .prefetch_related("sources", "styles")
    )
    return render(
        request,
        "walczak/compare.html",
        {
            "left": left,
            "right": right,
            "differences": key_differences(left, right, left_profile, right_profile),
            "pairs": paired_groups(profile_groups(left_profile), profile_groups(right_profile)),
            "studies": studies,
        },
    )


@require_http_methods(["GET"])
def golden(request: HttpRequest) -> HttpResponse:
    styles = Style.objects.filter(active=True, catalog_set="golden").prefetch_related("sources")
    return render(request, "walczak/golden.html", {"styles": styles})


@require_http_methods(["GET"])
def sitemap(request: HttpRequest) -> HttpResponse:
    """Public pages only. Session screens stay out of the index."""
    paths = [
        reverse("walczak:home"),
        reverse("walczak:list"),
        reverse("walczak:golden"),
        reverse("walczak:compare_form"),
    ]
    paths.extend(
        reverse("walczak:detail", args=[slug])
        for slug in Style.objects.filter(active=True).order_by("slug").values_list("slug", flat=True)
    )
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in paths:
        loc = escape(request.build_absolute_uri(path))
        lines.append(f"<url><loc>{loc}</loc></url>")
    lines.append("</urlset>")
    return HttpResponse("\n".join(lines), content_type="application/xml")


@require_http_methods(["GET"])
def fact(request: HttpRequest) -> HttpResponse:
    recent = request.session.get(FACT_KEY)
    recent_ids = [item for item in recent if isinstance(item, int)] if isinstance(recent, list) else []
    pool = Fact.objects.prefetch_related("styles", "sources").exclude(pk__in=recent_ids)
    picked = pool.order_by("?").first() or Fact.objects.prefetch_related("styles", "sources").order_by("?").first()
    if picked is not None:
        request.session[FACT_KEY] = [picked.pk, *[pk for pk in recent_ids if pk != picked.pk]][:5]
    return render(request, "walczak/fact.html", {"fact": picked})


def _forget(request: HttpRequest, key: str) -> None:
    if key in request.session:
        del request.session[key]


def _stored(row: dict) -> dict:
    beside = row.get("beside") or []
    return {
        "slug": row["slug"],
        "plus_pl": row["plus_pl"],
        "plus_en": row["plus_en"],
        "minus_pl": row["minus_pl"],
        "minus_en": row["minus_en"],
        "beside": [item["slug"] for item in beside if isinstance(item, dict) and isinstance(item.get("slug"), str)],
    }


def _hydrate(payload: object) -> list[dict]:
    if not isinstance(payload, list):
        return []
    slugs: list[str] = []
    for row in payload:
        if not isinstance(row, dict):
            continue
        slug = row.get("slug")
        if isinstance(slug, str):
            slugs.append(slug)
        for beside in row.get("beside") or []:
            if isinstance(beside, str):
                slugs.append(beside)
    styles = {style.slug: style for style in Style.objects.filter(slug__in=slugs, active=True)}
    rows = []
    for row in payload:
        if not isinstance(row, dict):
            continue
        style = styles.get(row.get("slug"))
        if style is None:
            continue
        plus = [{"pl": pl, "en": en} for pl, en in zip(row.get("plus_pl") or [], row.get("plus_en") or [], strict=False)]
        minus = [{"pl": pl, "en": en} for pl, en in zip(row.get("minus_pl") or [], row.get("minus_en") or [], strict=False)]
        beside = [styles[slug] for slug in row.get("beside") or [] if isinstance(slug, str) and slug in styles]
        rows.append({**row, "style": style, "plus": plus, "minus": minus, "beside": beside})
    return rows
