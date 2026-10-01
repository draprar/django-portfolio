import pytest

from poligon.framework import (
    COVERAGE_GATES,
    EXERCISE_TYPES_LIVE,
    EXERCISE_TYPES_RESERVED,
    LEVEL_PROFILES,
    PLACEMENT_QUESTION_COUNT,
    SCENARIOS,
    SKILLS,
    SRS_VERSION,
    competency_for,
    level_profile,
    load_glossary,
    scenario_by_id,
    score_band,
    suggest_placement_level,
)
from poligon.levels import LEVELS, level_names


def test_every_level_has_four_skill_competencies():
    assert set(LEVEL_PROFILES) == set(LEVELS)
    for level in LEVELS:
        profile = level_profile(level)
        assert profile is not None
        assert set(profile.competencies) == set(SKILLS)
        for skill in SKILLS:
            item = competency_for(level, skill)
            assert item is not None
            assert item.id
            assert item.text_en
            assert item.text_pl
            assert item.skill == skill
        assert profile.goal_en and profile.goal_pl
        assert profile.utterance_en and profile.utterance_pl
        assert profile.speed_en and profile.speed_pl
        assert profile.ambiguity_en and profile.ambiguity_pl
        assert profile.scenarios


def test_every_scenario_has_an_id_and_levels_only_use_those_ids():
    ids = [item.id for item in SCENARIOS]
    assert len(ids) == len(set(ids))
    for item in SCENARIOS:
        assert item.id
        assert item.name_en
        assert item.name_pl
        assert scenario_by_id(item.id) is item
    assert scenario_by_id("not-a-scenario") is None
    for profile in LEVEL_PROFILES.values():
        for scenario_id in profile.scenarios:
            assert scenario_by_id(scenario_id) is not None
    assert set(LEVEL_PROFILES[1].scenarios) < set(LEVEL_PROFILES[5].scenarios)


def test_unknown_level_has_no_label_and_no_profile():
    assert level_names(0) == ("", "")
    assert level_names(9) == ("", "")
    assert level_profile(0) is None
    assert competency_for(3, "X") is None


def test_task_types_keep_true_false_live_and_name_the_reserved_ones():
    assert EXERCISE_TYPES_LIVE == ("mcq", "listening", "speaking", "writing", "true_false")
    assert "true_false" not in EXERCISE_TYPES_RESERVED
    assert set(EXERCISE_TYPES_LIVE).isdisjoint(EXERCISE_TYPES_RESERVED)


def test_placement_v1_bands_cover_fifteen_questions():
    assert PLACEMENT_QUESTION_COUNT == 15
    assert [suggest_placement_level(n) for n in (0, 3, 4, 6, 7, 9, 10, 12, 13, 15)] == [
        1, 1, 2, 2, 3, 3, 4, 4, 5, 5,
    ]


def test_rubric_bands_are_three_words_not_a_percentage():
    assert score_band(0) == "needs_work"
    assert score_band(1) == "needs_work"
    assert score_band(2) == "developing"
    assert score_band(3) == "strong"
    assert score_band(4) == "strong"


def test_glossary_terms_are_unique_and_bilingual():
    rows = load_glossary()
    assert rows
    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids))
    for row in rows:
        assert row["en"] and row["pl"] and row["context"]
        assert row["en"] != row["pl"]


def test_named_versions_and_coverage_gates_stay_explicit():
    assert SRS_VERSION == "srs_v1"
    assert COVERAGE_GATES == (1, 8, 20)


@pytest.mark.django_db
def test_framework_does_not_change_the_start_page(client):
    response = client.get("/cwiczba/start/")
    assert response.status_code == 200
    assert "Przetrwanie" in response.content.decode()
