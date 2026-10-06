from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import escape
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

from wiciedzy.data.instruments import OPTIONAL_SCALE_ORDERS, PREFERENCE_SCALE_ANCHORS
from wiciedzy.display import (
    description_is_thin,
    key_differences,
    load_profile,
    paired_groups,
    profile_groups,
    region_labels,
    split_profile,
)
from wiciedzy.models import PreferenceQuestion, Study, Style, Tag
from wiciedzy.preference import answers_complete, rank_styles

PREFERENCE_KEY = "wiciedzy_preference"


@require_http_methods(["GET"])
def home(request: HttpRequest) -> HttpResponse:
    return render(request, "wiciedzy/home.html")


@require_http_methods(["GET"])
def style_list(request: HttpRequest) -> HttpResponse:
    tag_raw = request.GET.get("tag") or ""
    tags = list(Tag.objects.all())
    known_tags = {tag.slug for tag in tags}
    selected_tag = tag_raw if tag_raw in known_tags else ""
    styles = Style.objects.filter(active=True)
    if selected_tag:
        styles = styles.filter(tags__slug=selected_tag).distinct()
    return render(
        request,
        "wiciedzy/list.html",
        {
            "styles": styles,
            "tags": tags,
            "selected_tag": selected_tag,
            "compare_styles": Style.objects.filter(active=True, catalog_set="core").order_by("name_pl"),
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
    region_pl, region_en = region_labels(style.region)
    return render(
        request,
        "wiciedzy/detail.html",
        {
            "style": style,
            "relations": relations,
            "headline": headline,
            "rest": rest,
            "thin_sources": description_is_thin(style),
            "region_pl": region_pl,
            "region_en": region_en,
        },
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
        return render(request, "wiciedzy/empty.html")
    _attach_scale_anchors(questions)
    if request.method == "POST":
        if not answers_complete(questions, request.POST):
            _forget(request, PREFERENCE_KEY)
            return render(
                request,
                "wiciedzy/test.html",
                {"questions": questions, "total": len(questions), "error": True},
            )
        ranking = rank_styles(questions, request.POST)
        picks = ranking["picks"]
        if not picks:
            _forget(request, PREFERENCE_KEY)
            return render(
                request,
                "wiciedzy/test.html",
                {"questions": questions, "total": len(questions), "error": True},
            )
        request.session[PREFERENCE_KEY] = {"picks": [_stored(row) for row in picks]}
        return redirect("wiciedzy:match")
    return render(request, "wiciedzy/test.html", {"questions": questions, "total": len(questions)})


@require_http_methods(["GET"])
def preference_result(request: HttpRequest) -> HttpResponse:
    payload = request.session.get(PREFERENCE_KEY)
    if not isinstance(payload, dict):
        return redirect("wiciedzy:test")
    rows = _hydrate(payload.get("picks"))
    if not rows:
        return redirect("wiciedzy:test")
    return render(request, "wiciedzy/match.html", {"rows": rows})


@require_http_methods(["GET", "POST"])
def compare_form(request: HttpRequest) -> HttpResponse:
    styles = Style.objects.filter(active=True, catalog_set="core").order_by("name_pl")
    if request.method == "POST":
        left = request.POST.get("a") or ""
        right = request.POST.get("b") or ""
        known = set(styles.values_list("slug", flat=True))
        if left == right or left not in known or right not in known:
            return render(request, "wiciedzy/compare_form.html", {"styles": styles, "error": True})
        return redirect("wiciedzy:compare", a=left, b=right)
    return render(request, "wiciedzy/compare_form.html", {"styles": styles})


@require_http_methods(["GET"])
def compare(request: HttpRequest, a: str, b: str) -> HttpResponse:
    if a == b:
        styles = Style.objects.filter(active=True, catalog_set="core").order_by("name_pl")
        return render(request, "wiciedzy/compare_form.html", {"styles": styles, "error": True})
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
        "wiciedzy/compare.html",
        {
            "left": left,
            "right": right,
            "differences": key_differences(left, right, left_profile, right_profile),
            "pairs": paired_groups(profile_groups(left_profile), profile_groups(right_profile)),
            "studies": studies,
        },
    )


@require_http_methods(["GET"])
def sitemap(request: HttpRequest) -> HttpResponse:
    """Public pages only. Session screens stay out of the index."""
    paths = [
        reverse("wiciedzy:home"),
        reverse("wiciedzy:list"),
        reverse("wiciedzy:compare_form"),
    ]
    paths.extend(
        reverse("wiciedzy:detail", args=[slug])
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


def _attach_scale_anchors(questions: list[PreferenceQuestion]) -> None:
    for question in questions:
        question.is_required = (
            question.kind in {"scale", "ab", "situation"} and question.sort_order not in OPTIONAL_SCALE_ORDERS
        )
        row = PREFERENCE_SCALE_ANCHORS.get(question.sort_order, {})
        question.scale_hint_pl = row.get("hint_pl", "1 oznacza wcale, 5 — bardzo.")
        question.scale_hint_en = row.get("hint_en", "1 means not at all, 5 — very much.")
        question.scale_low_pl = row.get("anchor_low_pl", "wcale")
        question.scale_low_en = row.get("anchor_low_en", "not at all")
        question.scale_high_pl = row.get("anchor_high_pl", "bardzo")
        question.scale_high_en = row.get("anchor_high_en", "very much")


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
