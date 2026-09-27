import pytest
from django.core.management import call_command

from poligon.models import Exercise, Submission, VocabularyItem
from poligon.tests.factories import make_learner

EXPECTED_LEVELS = {0: 200, 1: 200, 2: 200, 3: 200, 4: 200, 5: 200}


@pytest.mark.django_db
def test_seed_poligon_is_bilingual_and_safe_to_repeat():
    call_command("seed_poligon")
    assert Exercise.objects.count() == 1200
    assert VocabularyItem.objects.count() == 1200
    assert Exercise.objects.filter(skill="L").count() == 300
    for level, count in EXPECTED_LEVELS.items():
        assert Exercise.objects.filter(level=level).count() == count
        assert VocabularyItem.objects.filter(level=level).count() == 200
    assert Exercise.objects.filter(level=0, content_source="wikipedia").count() == 0
    assert Exercise.objects.filter(content_source="wikipedia").count() >= 180
    assert not Exercise.objects.exclude(content_source="original").filter(attribution_en="").exists()
    assert not VocabularyItem.objects.exclude(content_source="original").filter(attribution_en="").exists()
    assert VocabularyItem.objects.filter(content_source="wiktionary").exclude(attribution_en="").count() >= 108

    exercise = Exercise.objects.get(slug="read-001-route")
    assert exercise.title_pl
    assert exercise.title_en
    assert exercise.prompt_pl != exercise.prompt_en
    assert exercise.options.count() == 4
    assert exercise.options.filter(text_pl="", text_en="").count() == 0
    item = VocabularyItem.objects.get(term="briefing")
    assert item.explanation_pl
    assert item.example_en

    learner = make_learner()
    Submission.objects.create(learner=learner, exercise=exercise, score=10)
    call_command("seed_poligon")
    assert Exercise.objects.count() == 1200
    assert VocabularyItem.objects.count() == 1200
    assert Exercise.objects.filter(skill="L").count() == 300
    assert Exercise.objects.filter(content_source="wikipedia").count() >= 180
    assert not Exercise.objects.exclude(content_source="original").filter(attribution_en="").exists()
    assert VocabularyItem.objects.filter(content_source="wiktionary").exclude(attribution_en="").count() >= 108
    assert Submission.objects.filter(learner=learner, exercise__slug="read-001-route").count() == 1
