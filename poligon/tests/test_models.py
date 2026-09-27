import pytest

from poligon.models import ChoiceOption, Review, StudyEvent
from poligon.tests.factories import make_learner, make_mcq, make_vocabulary


@pytest.mark.django_db
def test_bilingual_getters_follow_the_requested_language():
    exercise = make_mcq()
    option = ChoiceOption.objects.get(is_correct=True)
    item = make_vocabulary()
    state = make_learner()
    review = Review.objects.create(learner=state, item=item, due_at=state.created_at)
    event = StudyEvent.objects.create(learner=state, skill="L", minutes=2, note="note")

    assert exercise.get_title("en") == "Demo"
    assert exercise.get_title("pl") == "Demo PL"
    assert exercise.get_instructions("en") == "Read."
    assert exercise.get_prompt("pl") == "Pytanie po polsku."
    assert exercise.get_content("en") == ""
    assert exercise.get_category("pl") == "ruch"
    assert option.get_text("en") == "Correct choice"
    assert option.get_text("pl") == "Poprawna"
    assert item.get_explanation("pl") == "Krótkie spotkanie."
    assert item.get_example("en").startswith("The commander")
    assert item.get_category("en") == "command"
    assert str(state) == f"guest {state.guest_token} / 2222"
    assert str(review)
    assert str(event) == f"{state.pk} / L"
    assert str(option) == "Correct choice"
    assert str(item) == "briefing"
