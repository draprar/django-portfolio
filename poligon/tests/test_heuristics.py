from poligon.heuristics import HEURISTIC_NOTE, assess_language_sample, coaching_hint


def test_assessor_returns_metrics():
    result = assess_language_sample(
        "First we move to the site. Then we check the equipment and report to the commander.",
    )
    assert result["sentence_count"] == 2
    assert result["overall"] > 0
    assert result["note"] == HEURISTIC_NOTE


def test_assessor_handles_empty_text_and_explicit_minutes():
    result = assess_language_sample("", minutes=2)
    assert result["word_count"] == 0
    assert result["words_per_minute"] == 0
    assert "not an official" in str(result["note"])


def test_the_hint_names_the_weakest_thing_first():
    short = coaching_hint(assess_language_sample("Water."))
    assert "za krótko" in short[1]

    filler = coaching_hint(assess_language_sample("Um, um, um. " + "The team moves to the site. " * 6))
    assert "wypełniaczy" in filler[1]

    unlinked = coaching_hint(assess_language_sample("The team moves out. The truck waits here. " * 6))
    assert "łączy" in unlinked[1]

    repeated = coaching_hint(assess_language_sample("Water water water because water water. " * 6))
    assert "wracają" in repeated[1]


def test_a_decent_sample_gets_encouragement_not_a_correction():
    text = (
        "First the team confirms the water, because nothing starts without it. "
        "Then we check the trucks and radios, although the gate may still be shut. "
        "Finally the shift leader signs the sheet and we move to the northern site."
    )
    english, polish = coaching_hint(assess_language_sample(text))
    assert "Keep this length" in english
    assert "Zachowaj" in polish


def test_the_hint_survives_a_submission_without_metrics():
    english, polish = coaching_hint({})
    assert english and polish
