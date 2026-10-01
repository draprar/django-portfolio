from poligon.heuristics import (
    EVALUATOR_VERSION,
    HEURISTIC_NOTE,
    assess_language_sample,
    coaching_hint,
    recorded_evaluator_version,
)


def test_assessor_returns_metrics():
    result = assess_language_sample(
        "First we move to the site. Then we check the equipment and report to the commander.",
    )
    assert result["sentence_count"] == 2
    assert result["overall"] > 0
    assert result["note"] == HEURISTIC_NOTE
    assert result["evaluator_version"] == EVALUATOR_VERSION
    assert recorded_evaluator_version({}) == EVALUATOR_VERSION
    assert recorded_evaluator_version({"evaluator_version": "writing_eval_v2"}) == "writing_eval_v2"


def test_assessor_handles_empty_text_and_explicit_minutes():
    result = assess_language_sample("", minutes=2)
    assert result["word_count"] == 0
    assert result["words_per_minute"] == 0
    assert "not an official" in str(result["note"])


def test_a_short_sample_is_told_it_is_too_short():
    short = coaching_hint(assess_language_sample("Water."))
    assert "za krótko" in short[1]
    assert "wypełniaczy" not in short[1]
    assert "synonim" not in short[1]


def test_a_decent_sample_describes_the_shape_and_stops_there():
    text = (
        "First the team confirms the water, because nothing starts without it. "
        "Then we check the trucks and radios, although the gate may still be shut. "
        "Finally the shift leader signs the sheet and we move to the northern site. "
        "After that the spare cans go on the second truck before the convoy leaves."
    )
    english, polish = coaching_hint(assess_language_sample(text))
    assert "shape of the text is fine" in english
    assert "nie jest sprawdzana automatycznie" in polish
    assert "synonim" not in polish


def test_level_five_asks_for_more_words_than_level_one():
    sample = assess_language_sample("The gate is shut. The water is here. The team is ready now.")
    fine_en, fine_pl = coaching_hint(sample, 1)
    short_en, short_pl = coaching_hint(sample, 5)
    assert "shape of the text is fine" in fine_en
    assert "w porządku" in fine_pl
    assert "too short" in short_en
    assert "za krótko" in short_pl


def test_the_hint_survives_a_submission_without_metrics():
    english, polish = coaching_hint({})
    assert english and polish
    assert "za krótko" in polish
