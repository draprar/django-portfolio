from poligon.models import ChoiceOption, Exercise, LearnerState, VocabularyItem


def make_learner(**overrides) -> LearnerState:
    return LearnerState.objects.create(**overrides)


def make_exercise(**overrides) -> Exercise:
    data = {
        "slug": "demo",
        "title_pl": "Demo PL",
        "title_en": "Demo",
        "skill": "R",
        "level": 2,
        "exercise_type": "mcq",
        "instructions_pl": "Czytaj.",
        "instructions_en": "Read.",
        "prompt_pl": "Pytanie po polsku.",
        "prompt_en": "Question in English.",
        "content_pl": "",
        "content_en": "",
        "category_pl": "ruch",
        "category_en": "movement",
        "source_note": "Original Poligon",
    }
    data.update(overrides)
    return Exercise.objects.create(**data)


def make_mcq(**overrides) -> Exercise:
    exercise = make_exercise(**overrides)
    ChoiceOption.objects.create(
        exercise=exercise,
        text_pl="Poprawna",
        text_en="Correct choice",
        is_correct=True,
        sort_order=0,
    )
    ChoiceOption.objects.create(
        exercise=exercise,
        text_pl="Błędna",
        text_en="Wrong choice",
        is_correct=False,
        sort_order=1,
    )
    return exercise


def make_vocabulary(**overrides) -> VocabularyItem:
    data = {
        "term": "briefing",
        "translation": "odprawa",
        "explanation_pl": "Krótkie spotkanie.",
        "explanation_en": "A short meeting.",
        "example_pl": "Dowódca dał odprawę.",
        "example_en": "The commander gave a briefing.",
        "category_pl": "dowodzenie",
        "category_en": "command",
    }
    data.update(overrides)
    return VocabularyItem.objects.create(**data)
