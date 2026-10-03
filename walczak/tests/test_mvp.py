from io import StringIO
from pathlib import Path

import pytest
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.urls import reverse

from walczak.data.styles import FACTS
from walczak.dimensions import DIMENSION_LABELS
from walczak.humor import choose_archetypes
from walczak.models import (
    Fact,
    HumorQuestion,
    IPIPItem,
    PreferenceQuestion,
    Source,
    Style,
    StyleRelation,
    StyleType,
    TrainingProfile,
)
from walczak.preference import _reading_list, _reasons, _sort_key, answers_complete, rank_styles, user_vector
from walczak.psychology import score_ipip


def load_catalog() -> None:
    call_command("import_walczak")


def answered(questions, high_dimensions: set[str] | None = None) -> dict[str, str]:
    high = high_dimensions or set()
    posted: dict[str, str] = {}
    for question in questions:
        if question.kind == "scale":
            posted[f"s{question.pk}"] = "5" if question.dimension in high else "1"
        elif question.kind in {"ab", "situation"}:
            option = question.options.all()[0]
            posted[f"q{question.pk}"] = str(option.pk)
    return posted


@pytest.mark.django_db
def test_profile_rejects_six_and_slug_stays_unique():
    with pytest.raises(IntegrityError), transaction.atomic():
        Style.objects.create(
            slug="boks",
            name_pl="Inny",
            name_en="Other",
            family="uderzenia",
            summary_pl="Opis.",
            summary_en="Summary.",
        )
    style = Style.objects.create(
        slug="poza-katalogiem",
        name_pl="Poza",
        name_en="Outside",
        family="uderzenia",
        summary_pl="Opis.",
        summary_en="Summary.",
    )
    kind = StyleType.objects.create(code="hybrid-test", name_pl="Mieszanka", name_en="Hybrid")
    style.style_types.add(kind)

    assert style.style_types.filter(code="hybrid-test").exists()

    profile = TrainingProfile(style=style, striking=6)
    with pytest.raises(ValidationError):
        profile.full_clean()


@pytest.mark.django_db
def test_relation_clean_requires_a_source():
    boks = Style.objects.get(slug="boks")
    judo = Style.objects.get(slug="judo")
    relation = StyleRelation.objects.create(from_style=boks, to_style=judo, kind="related")

    with pytest.raises(ValidationError):
        relation.full_clean()

    relation.sources.add(boks.sources.get())
    relation.full_clean()


@pytest.mark.django_db
def test_import_is_stable_and_validation_passes():
    load_catalog()
    boks = Style.objects.get(slug="boks")
    source_count = boks.sources.count()
    relation_count = StyleRelation.objects.count()
    load_catalog()

    assert Style.objects.filter(catalog_set="core", active=True).count() == 30
    assert Style.objects.filter(catalog_set="golden", active=True).count() == 10
    assert Style.objects.filter(slug="boks").count() == 1
    assert boks.sources.count() == source_count
    assert Source.objects.filter(style=boks).count() == source_count
    assert StyleRelation.objects.count() == relation_count
    assert StyleRelation.objects.filter(from_style__slug="sanda", kind="modern_form").exists()
    assert not StyleRelation.objects.filter(from_style__slug="sanda", kind="subset").exists()
    assert StyleRelation.objects.filter(from_style__slug="bjj", kind="influenced").exists()
    assert Fact.objects.count() == len(FACTS)
    assert Style.objects.get(slug="boks").facts.count() == 1
    capoeira = Style.objects.get(slug="capoeira")
    assert set(capoeira.tags.values_list("slug", flat=True)) >= {"striking", "traditional", "solo"}
    hema = Style.objects.get(slug="hema")
    assert set(hema.tags.values_list("slug", flat=True)) >= {"weapons", "historical"}
    output = StringIO()
    call_command("validate_walczak_content", stdout=output)
    report = output.getvalue()
    assert "ERROR:" not in report
    assert "WARNING:" in report
    assert "discovery" in report


@pytest.mark.django_db
def test_validation_fails_before_the_catalog_is_loaded():
    with pytest.raises(SystemExit):
        call_command("validate_walczak_content")


@pytest.mark.django_db
def test_preference_rank_is_stable_and_skips_a_style_without_a_profile():
    load_catalog()
    bare = Style.objects.create(
        slug="bez-profilu",
        name_pl="Bez profilu",
        name_en="No profile",
        family="uderzenia",
        summary_pl="Opis.",
        summary_en="Summary.",
        catalog_set="core",
    )
    questions = list(PreferenceQuestion.objects.filter(active=True).prefetch_related("options__weights"))
    assert rank_styles(questions, {})["picks"] == []
    posted = answered(questions, {"striking"})
    first = rank_styles(questions, posted)
    second = rank_styles(questions, posted)
    first_slugs = [row["slug"] for row in first["picks"]]
    second_slugs = [row["slug"] for row in second["picks"]]

    assert first_slugs == second_slugs
    assert first_slugs == [row["slug"] for row in rank_styles(questions, posted)["picks"]]
    assert first_slugs
    assert bare.slug not in first_slugs
    assert len(first_slugs) <= 5
    assert "score" not in first["picks"][0]
    assert "band" not in first["picks"][0]


@pytest.mark.django_db
def test_striking_preference_ranks_boxing_above_judo():
    load_catalog()
    questions = list(PreferenceQuestion.objects.filter(active=True).prefetch_related("options__weights"))
    posted = answered(questions, {"striking", "contact_level", "competition_level"})
    ranked = {row["slug"]: row for row in rank_styles(questions, posted)["picks"]}
    labels = {label for pair in DIMENSION_LABELS.values() for label in pair}
    families: dict[str, int] = {}
    for row in ranked.values():
        families[row["family"]] = families.get(row["family"], 0) + 1

    user = user_vector(questions, posted)

    def distance(slug: str) -> float:
        profile = TrainingProfile.objects.get(style__slug=slug)
        vector = profile.as_vector()
        shared = [name for name in user if name in vector]
        return sum(abs(user[name] - vector[name]) for name in shared) / len(shared)

    assert distance("boks") < distance("judo")
    assert "boks" in ranked
    assert ranked["boks"]["plus_pl"]
    assert len(ranked["boks"]["plus_pl"]) <= 3
    assert len(ranked["boks"]["minus_pl"]) <= 2
    assert all("stój" not in line for line in ranked["boks"]["plus_pl"])
    assert all(line.strip(" .") not in labels for line in ranked["boks"]["plus_pl"])
    assert all("osi:" not in line for line in ranked["boks"]["minus_pl"])
    assert all(count <= 2 for count in families.values())


@pytest.mark.django_db
def test_personality_score_does_not_change_the_preference_rank():
    load_catalog()
    questions = list(PreferenceQuestion.objects.filter(active=True).prefetch_related("options__weights"))
    posted = answered(questions, {"striking", "grappling", "contact_level"})
    before = [row["slug"] for row in rank_styles(questions, posted)["picks"]]

    items = list(IPIPItem.objects.select_related("scale"))
    answers = {item.pk: 5 for item in items}
    assert score_ipip(items, answers) == score_ipip(items, answers)
    after = [row["slug"] for row in rank_styles(questions, posted)["picks"]]
    assert before == after


@pytest.mark.django_db
def test_reverse_ipip_item_flips_the_point():
    load_catalog()
    item = IPIPItem.objects.select_related("scale").filter(reverse=True).first()
    assert item is not None
    scored = score_ipip([item], {item.pk: 1})

    assert scored[item.scale.code] == 5


@pytest.mark.django_db
def test_compare_without_a_study_says_there_is_no_data(client):
    load_catalog()
    response = client.get(reverse("walczak:compare", args=["boks", "judo"]))
    content = response.content.decode()

    assert response.status_code == 200
    assert "walczak-scale-legend" in content
    assert "prawie nie występuje albo niewielkie nastawienie" in content
    assert "Historia i typ" in content
    assert "Psychologia / badania" not in content
    assert "Szybki profil" not in content
    assert content.index("Historia i typ") < content.index("Techniki i trening")
    assert "<canvas" not in content

    same = client.post(reverse("walczak:compare_form"), {"a": "boks", "b": "boks"})
    assert "Wybierz dwa różne style z zestawu głównego." in same.content.decode()
    direct = client.get(reverse("walczak:compare", args=["boks", "boks"]))
    assert direct.status_code == 200
    assert "Wybierz dwa różne style z zestawu głównego." in direct.content.decode()
    assert client.get(reverse("walczak:compare", args=["boks", "dambe"])).status_code == 404
    assert client.get(reverse("walczak:compare", args=["boks", "nie-ma-stylu"])).status_code == 404


@pytest.mark.django_db
def test_humor_post_is_stable_and_ignores_the_matcher():
    load_catalog()
    source = Path("walczak/humor.py").read_text(encoding="utf-8")
    assert "walczak.preference" not in source
    assert "rank_styles" not in source
    questions = list(HumorQuestion.objects.filter(active=True).prefetch_related("choices"))
    posted = {}
    for question in questions:
        choice = question.choices.order_by("sort_order").first()
        assert choice is not None
        posted[f"q{question.pk}"] = str(choice.pk)
    first = choose_archetypes(questions, posted)
    second = choose_archetypes(questions, posted)

    assert first and second
    assert [item.slug for item in first] == [item.slug for item in second] == ["chce-miecz"]
    assert choose_archetypes(questions, {}) == []


@pytest.mark.django_db
def test_cards_golden_and_fact(client):
    load_catalog()
    detail = client.get(reverse("walczak:detail", args=["kyokushin"]))
    content = detail.content.decode()
    assert "Pochodzenie" in content
    assert "Karate" in content
    assert "https://en.wikipedia.org/wiki/Kyokushin" in content

    golden = client.get("/walczak/zlote/")
    fact = client.get("/walczak/fakt/")
    assert golden.status_code == 404
    assert fact.status_code == 404


@pytest.mark.django_db
def test_read_only_api_lists_styles_and_a_fact(client):
    load_catalog()
    listing = client.get(reverse("walczak:api-styles"))
    payload = listing.json()

    assert listing.status_code == 200
    assert len(payload) >= 40
    assert any(row["slug"] == "boks" for row in payload)
    assert "catalog_set" not in payload[0]
    assert client.post(reverse("walczak:api-styles")).status_code == 405

    detail = client.get(reverse("walczak:api-style", args=["szermierka"]))
    body = detail.json()
    assert body["name_en"] == "Sport fencing"
    assert "catalog_set" not in body
    assert "joke_pl" not in body
    assert len(body["sources"]) >= 2
    assert "quality" not in body["sources"][0]
    assert client.get(reverse("walczak:api-style", args=["nie-ma-stylu"])).status_code == 404

    tags = client.get(reverse("walczak:api-tags"))
    assert tags.status_code == 200

    fact = client.get(reverse("walczak:api-fact"))
    assert fact.status_code == 200
    assert fact.json()["text_pl"]


@pytest.mark.django_db
def test_tag_filter_and_umbrella_label(client):
    load_catalog()
    listed = client.get(reverse("walczak:list"), {"tag": "historical"})
    page = listed.content.decode()
    assert listed.status_code == 200
    assert "HEMA" in page
    assert reverse("walczak:detail", args=["hema"]) in page
    assert reverse("walczak:detail", args=["boks"]) not in page

    karate = client.get(reverse("walczak:detail", args=["karate"]))
    karate_page = karate.content.decode()
    assert "To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali." in karate_page
    assert "To moja ocena" not in karate_page
    assert "Pokaż pełny profil" in karate.content.decode()


@pytest.mark.django_db
def test_every_core_style_can_be_either_side_of_a_comparison(client):
    load_catalog()
    slugs = list(Style.objects.filter(catalog_set="core", active=True).values_list("slug", flat=True))
    assert len(slugs) >= 30
    for slug in slugs:
        other = "judo" if slug == "boks" else "boks"
        as_left = client.get(reverse("walczak:compare", args=[slug, other]))
        as_right = client.get(reverse("walczak:compare", args=[other, slug]))
        assert as_left.status_code == 200
        assert as_right.status_code == 200
        assert "<canvas" not in as_left.content.decode()


@pytest.mark.django_db
def test_fact_draw_skips_the_previous_one(client):
    load_catalog()
    first = client.get("/walczak/fakt/")
    second = client.get("/walczak/fakt/")
    assert first.status_code == 404
    assert second.status_code == 404


@pytest.mark.django_db
def test_serious_pages_do_not_call_the_catalog_a_joke(client):
    load_catalog()
    home = client.get(reverse("walczak:home")).content.decode()
    assert "To żart" not in home
    assert "Siemasz na Walczaku, obczaj niżej." in home
    assert "Archetyp" not in home
    assert "Quizopasowanie" in home


@pytest.mark.django_db
def test_incomplete_preference_does_not_open_a_list(client):
    load_catalog()
    questions = list(PreferenceQuestion.objects.filter(active=True).prefetch_related("options__weights"))
    empty = client.post(reverse("walczak:test"), {})
    assert empty.status_code == 200
    assert "Dopiero wtedy pokaże się lista." in empty.content.decode()
    assert "walczak_preference" not in client.session

    scale = next(question for question in questions if question.kind == "scale")
    partial = client.post(reverse("walczak:test"), {f"s{scale.pk}": "3"})
    assert partial.status_code == 200
    assert not answers_complete(questions, {f"s{scale.pk}": "3"})

    posted = answered(questions, {"weapons"})
    assert answers_complete(questions, posted)
    opened = client.post(reverse("walczak:test"), posted)
    assert opened.status_code == 302
    page = client.get(reverse("walczak:match")).content.decode()
    assert "Do poczytania" in page
    assert "22 osie" not in page
    assert "Wysokie dopasowanie" not in page
    assert "moja ocena" not in page
    assert "Quizopasowanie" in page
    assert 'name="robots" content="noindex"' in page
    forgotten = client.post(reverse("walczak:test"), {})
    assert forgotten.status_code == 200
    assert "walczak_preference" not in client.session
    again = client.get(reverse("walczak:match"))
    assert again.status_code == 302
    assert again.url == reverse("walczak:test")


@pytest.mark.django_db
def test_low_agreement_and_striking_copy_do_not_say_stance():
    plus_pl, _, _, _ = _reasons({"weapons": 0.0}, {"weapons": 0}, ["weapons"])
    striking, _, _, _ = _reasons({"striking": 5.0}, {"striking": 5}, ["striking"])

    assert plus_pl == ["Broni jest tu prawie nie ma — i dobrze, bo właśnie tego szukasz."]
    assert "uderz" in striking[0].lower()
    assert "stój" not in striking[0]


def test_equal_distance_breaks_the_tie_by_slug():
    def row(slug: str, family: str, distance: float) -> dict:
        style = type("StyleStub", (), {"slug": slug, "name_pl": slug, "name_en": slug})()
        return {"slug": slug, "style": style, "distance": distance, "family": family, "beside": []}

    rows = [
        row("zeta", "uderzenia", 1.0),
        row("alfa", "chwyty", 1.0),
        row("boks", "uderzenia", 0.5),
    ]
    rows.sort(key=_sort_key)
    picks = _reading_list(rows, set())

    assert [item["slug"] for item in picks] == ["boks", "alfa", "zeta"]
    assert _sort_key(row("alfa", "chwyty", 1.0)) < _sort_key(row("zeta", "uderzenia", 1.0))


def test_related_style_becomes_a_link_not_a_second_card():
    def row(slug: str, family: str, distance: float) -> dict:
        style = type("StyleStub", (), {"slug": slug, "name_pl": slug, "name_en": slug})()
        return {"slug": slug, "style": style, "distance": distance, "family": family, "beside": []}

    picks = _reading_list(
        [
            row("hema", "bron", 0.1),
            row("szermierka", "bron", 0.2),
            row("kendo", "bron", 0.3),
            row("boks", "uderzenia", 0.4),
            row("judo", "chwyty", 0.5),
            row("zapasy", "chwyty", 0.6),
        ],
        {frozenset(("hema", "szermierka"))},
    )
    slugs = [item["slug"] for item in picks]

    assert slugs[0] == "hema"
    assert "szermierka" not in slugs
    assert picks[0]["beside"][0]["slug"] == "szermierka"
    assert len(picks) == 5
    assert sum(1 for item in picks if item["family"] == "bron") <= 2


@pytest.mark.django_db
def test_list_hides_the_second_person_joke_and_names_the_thin_source(client):
    load_catalog()
    listed = client.get(reverse("walczak:list")).content.decode()
    assert "nie lubisz zostawiać spraw niedokończonych" not in listed
    assert "sport walki na pięści" in listed
    assert "Mniej oczywiste" not in listed
    assert "Losowy fakt" not in listed
    assert "Bökh" in listed

    muay = client.get(reverse("walczak:detail", args=["muay-thai"])).content.decode()
    assert "ośmiu kończyn" in muay
    assert "ośmiu broni" not in muay

    krav = client.get(reverse("walczak:detail", args=["krav-maga"])).content.decode()
    assert "drugie źródło tylko wspomina o tym temacie" in krav
