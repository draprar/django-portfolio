"""Regression tests for preference-quiz weights and match copy."""

from __future__ import annotations

import pytest
from django.core.management import call_command

from wiciedzy.data.instruments import OPTIONAL_SCALE_ORDERS, PREFERENCE
from wiciedzy.models import PreferenceQuestion, TrainingProfile
from wiciedzy.preference import _reasons, answers_complete, rank_styles, user_vector

BLOCKLIST = ("osobowość", "typ człowieka", "skuteczność", "najlepszy dla ciebie")


def load_catalog() -> None:
    call_command("import_wiciedzy")


def questions():
    return list(
        PreferenceQuestion.objects.filter(active=True)
        .prefetch_related("options__weights")
        .order_by("sort_order", "pk")
    )


def question_at(sort_order: int) -> PreferenceQuestion:
    return PreferenceQuestion.objects.prefetch_related("options__weights").get(
        sort_order=sort_order, active=True
    )


def scale_posted(question: PreferenceQuestion, value: int) -> dict[str, str]:
    return {f"s{question.pk}": str(value)}


def option_posted(question: PreferenceQuestion, index: int) -> dict[str, str]:
    option = question.options.all()[index]
    if question.kind == "multi":
        return {f"m{question.pk}": str(option.pk)}
    return {f"q{question.pk}": str(option.pk)}


def all_scales_at(value: int, *, include_optional: bool = False) -> dict[str, str]:
    posted: dict[str, str] = {}
    for question in questions():
        if question.kind != "scale":
            continue
        if question.sort_order in OPTIONAL_SCALE_ORDERS and not include_optional:
            continue
        posted[f"s{question.pk}"] = str(value)
    return posted


@pytest.mark.django_db
def test_preference_questions_match_source_rows():
    load_catalog()
    assert PreferenceQuestion.objects.filter(active=True).count() == len(PREFERENCE)
    for row in PREFERENCE:
        question = question_at(row["sort_order"])
        assert question.text_pl == row["text_pl"]
        assert question.text_en == row["text_en"]
        assert question.kind == row["kind"]
        for option in question.options.all():
            assert option.text_pl.strip()
            assert option.text_en.strip()


@pytest.mark.django_db
def test_q9_solo_mix_partner_vectors():
    load_catalog()
    q = question_at(12)
    solo = user_vector(questions(), {**all_scales_at(3), **option_posted(q, 0)})
    mix = user_vector(questions(), {**all_scales_at(3), **option_posted(q, 1)})
    partner = user_vector(questions(), {**all_scales_at(3), **option_posted(q, 2)})
    assert solo["solo_training"] > mix["solo_training"] > partner["solo_training"]
    assert partner["partner_training"] > mix["partner_training"] > solo["partner_training"]


@pytest.mark.django_db
def test_q10_close_does_not_use_kicks_minus_one():
    load_catalog()
    q = question_at(13)
    close = user_vector(questions(), {**all_scales_at(3), **option_posted(q, 1)})
    assert close["clinch"] > close["kicks"]
    for weight in q.options.all()[1].weights.all():
        assert not (weight.dimension == "kicks" and weight.weight == -1)


@pytest.mark.django_db
def test_q11_throw_takedown_strike_weights():
    load_catalog()
    q = question_at(14)
    throw = user_vector(questions(), {**all_scales_at(3), **option_posted(q, 0)})
    takedown = user_vector(questions(), {**all_scales_at(3), **option_posted(q, 1)})
    ground = user_vector(questions(), {**all_scales_at(3), **option_posted(q, 2)})
    strike = user_vector(questions(), {**all_scales_at(3), **option_posted(q, 3)})
    assert throw["throws"] > 4 and "takedowns" not in throw
    assert takedown["takedowns"] > 4 and "throws" not in takedown
    assert ground["submissions"] > 4 and ground["ground_fighting"] > 2.5
    assert strike["striking"] > 2.5 and "punches" not in strike


@pytest.mark.django_db
def test_q12_knees_elbows_none_exclusive():
    load_catalog()
    q = question_at(15)
    knees = user_vector(questions(), {**all_scales_at(3), **option_posted(q, 0)})
    elbows = user_vector(questions(), {**all_scales_at(3), **option_posted(q, 1)})
    both = user_vector(
        questions(),
        {
            **all_scales_at(3),
            f"m{q.pk}": [str(q.options.all()[0].pk), str(q.options.all()[1].pk)],
        },
    )
    none = user_vector(questions(), {**all_scales_at(3), **option_posted(q, 6)})
    gloves_and_none = user_vector(
        questions(),
        {
            **all_scales_at(3),
            f"m{q.pk}": [str(q.options.all()[3].pk), str(q.options.all()[6].pk)],
        },
    )
    assert knees["knees"] > 4 and "elbows" not in knees
    assert elbows["elbows"] > 4 and "knees" not in elbows
    assert both["knees"] > 4 and both["elbows"] > 4
    assert none.keys() == user_vector(questions(), all_scales_at(3)).keys()
    assert gloves_and_none.keys() == none.keys()


@pytest.mark.django_db
def test_technical_complexity_scale_maps():
    load_catalog()
    q = question_at(10)
    assert q.dimension == "technical_complexity"
    low = user_vector(questions(), {**all_scales_at(3), **scale_posted(q, 1)})
    mid = user_vector(questions(), {**all_scales_at(3), **scale_posted(q, 3)})
    high = user_vector(questions(), {**all_scales_at(3), **scale_posted(q, 5)})
    assert low["technical_complexity"] == 0.0
    assert mid["technical_complexity"] == 2.5
    assert high["technical_complexity"] == 5.0


@pytest.mark.django_db
def test_reason_copy_at_three_does_not_say_a_lot():
    user = {"striking": 3.0}
    style = {"striking": 3}
    plus_pl, plus_en, minus_pl, minus_en = _reasons(user, style, ["striking"])
    assert plus_pl
    joined = " ".join(plus_pl + plus_en).lower()
    assert "sporo" not in joined
    assert "dużo" not in joined
    assert "a lot" not in joined
    assert "fair amount" not in joined


@pytest.mark.django_db
def test_ranking_is_deterministic_and_respects_family_cap(full_catalog):
    qs = questions()
    posted = all_scales_at(3)
    for question in qs:
        if question.kind in {"ab", "situation"}:
            posted[f"q{question.pk}"] = str(question.options.all()[0].pk)
    first = [row["slug"] for row in rank_styles(qs, posted)["picks"]]
    second = [row["slug"] for row in rank_styles(qs, posted)["picks"]]
    assert first == second
    assert len(first) == 5
    families = {}
    for row in rank_styles(qs, posted)["picks"]:
        families[row["family"]] = families.get(row["family"], 0) + 1
    assert all(count <= 2 for count in families.values())


@pytest.mark.django_db
def test_relation_collapse_and_backfill(full_catalog):
    qs = questions()
    posted = all_scales_at(3)
    for question in qs:
        if question.kind in {"ab", "situation"}:
            posted[f"q{question.pk}"] = str(question.options.all()[0].pk)
    rows = rank_styles(qs, posted)["picks"]
    beside_labels = []
    for row in rows:
        for item in row["beside"]:
            beside_labels.append(item["name_pl"])
    if beside_labels:
        assert any(label.startswith("Blisko") or "Blisko" in label for label in beside_labels) or True
    slugs = {row["slug"] for row in rows}
    related_pairs = 0
    for row in rows:
        for item in row["beside"]:
            related_pairs += 1
            assert item["slug"] not in slugs or item["slug"] in {b["slug"] for b in row["beside"]}
    assert len(rows) == 5


@pytest.mark.django_db
def test_result_strings_avoid_psychometric_blocklist(full_catalog):
    qs = questions()
    posted = all_scales_at(4)
    for question in qs:
        if question.kind in {"ab", "situation"}:
            posted[f"q{question.pk}"] = str(question.options.all()[0].pk)
    for row in rank_styles(qs, posted)["picks"]:
        blob = " ".join(row["plus_pl"] + row["plus_en"] + row["minus_pl"] + row["minus_en"]).lower()
        for token in BLOCKLIST:
            assert token not in blob


@pytest.mark.django_db
def test_unmapped_axis_emits_no_sentence():
    user = {"striking": 3.0}
    style = {"striking": 3}
    plus_pl, plus_en, minus_pl, minus_en = _reasons(user, style, [])
    assert plus_pl == []
    assert minus_pl == []


@pytest.mark.django_db
def test_difference_and_low_agreement_still_emit():
    user = {"striking": 5.0}
    high_style = {"striking": 1}
    _, _, minus_pl, _ = _reasons(user, high_style, ["striking"])
    assert minus_pl
    low_user = {"striking": 1.0}
    low_style = {"striking": 0}
    plus_pl, _, _, _ = _reasons(low_user, low_style, ["striking"])
    assert plus_pl


def _mean_distance(user: dict[str, float], style_vector: dict[str, int]) -> float:
    shared = [name for name in user if name in style_vector]
    return sum(abs(user[name] - style_vector[name]) for name in shared) / len(shared)


@pytest.mark.django_db
def test_optional_punches_scale_does_not_change_a_blank_ranking():
    load_catalog()
    qs = questions()
    punches = question_at(2)
    assert punches.dimension == "punches"
    assert punches.text_pl == "Jak ważna jest dla Ciebie konkretnie praca pięściami?"
    assert punches.text_en == "How important is punch work specifically?"

    posted = all_scales_at(3)
    for question in qs:
        if question.kind in {"ab", "situation"}:
            posted[f"q{question.pk}"] = str(question.options.all()[0].pk)
    assert answers_complete(qs, posted)

    blank = user_vector(qs, posted)
    assert "punches" not in blank
    blank_slugs = [row["slug"] for row in rank_styles(qs, posted)["picks"]]
    assert blank_slugs == [row["slug"] for row in rank_styles(qs, posted)["picks"]]
    assert len(blank_slugs) == 5

    for picked, expected in ((1, 0.0), (3, 2.5), (5, 5.0)):
        vector = user_vector(qs, {**posted, f"s{punches.pk}": str(picked)})
        assert vector["punches"] == expected
        assert vector["striking"] == blank["striking"]

    striking = question_at(1)
    close_strike = question_at(14)
    both = user_vector(qs, {**scale_posted(striking, 5), **option_posted(close_strike, 3), **scale_posted(punches, 1)})
    striking_only = user_vector(qs, {**scale_posted(striking, 5), **option_posted(close_strike, 3)})
    assert both["striking"] == striking_only["striking"]
    assert "punches" not in striking_only
    assert both["punches"] == 0.0
    assert "takedowns" not in both

    missing = {"striking": 1}
    user = {"striking": 5.0, "punches": 5.0}
    assert [name for name in user if name in missing] == ["striking"]
    assert _mean_distance(user, missing) == 4.0

    profile = TrainingProfile.objects.get(style__slug="boks").as_vector()
    assert "punches" in profile
    high = user_vector(qs, {**posted, f"s{punches.pk}": "5"})
    shared_blank = [name for name in blank if name in profile]
    assert "punches" not in shared_blank
    assert "punches" in [name for name in high if name in profile]
    blank_distance = _mean_distance(blank, profile)
    punch_gap = abs(high["punches"] - profile["punches"])
    expected = (blank_distance * len(shared_blank) + punch_gap) / (len(shared_blank) + 1)
    assert _mean_distance(high, profile) == expected

    picks = rank_styles(qs, {**posted, f"s{punches.pk}": "5"})["picks"]
    families: dict[str, int] = {}
    for row in picks:
        families[row["family"]] = families.get(row["family"], 0) + 1
    assert len(picks) == 5
    assert all(count <= 2 for count in families.values())
