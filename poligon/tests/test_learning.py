import pytest
from django.urls import reverse

from poligon.learning import assess_writing_v2, one_improvement
from poligon.models import ProductEvent, Submission
from poligon.tests.factories import make_exercise, make_mcq


def test_writing_v2_names_one_missing_fact():
    feedback = assess_writing_v2(
        "We hold at the north gate and we wait there with the team. " * 6,
        ["north gate", "eight"],
    )
    assert feedback["evaluator_version"] == "writing_eval_v2"
    assert feedback["criteria"][0]["met"] is True
    assert feedback["criteria"][1]["met"] is False
    assert feedback["overall_band"] in {"needs_work", "developing", "strong"}
    _en, pl = one_improvement(feedback, level=2)
    assert pl == "Dopisz ten fakt: eight."
    assert "north gate" not in pl


@pytest.mark.django_db
def test_a_true_or_false_item_is_scored_like_a_choice(member_client):
    exercise = make_exercise(slug="gate-tf", exercise_type="true_false", skill="R")
    from poligon.models import ChoiceOption

    ChoiceOption.objects.create(exercise=exercise, text_en="True", text_pl="True", is_correct=True)
    ChoiceOption.objects.create(exercise=exercise, text_en="False", text_pl="False", is_correct=False)
    posted = member_client.post(
        reverse("poligon:exercise", args=[exercise.slug]),
        {"option_id": exercise.options.get(text_en="True").pk},
    )
    content = member_client.get(posted.url).content.decode()
    assert "Dobrze" in content
    assert "Następny krok" in content


@pytest.mark.django_db
def test_an_empty_answer_is_rejected_on_the_server(member_client):
    exercise = make_exercise(slug="write-empty", skill="W", exercise_type="writing")
    page = member_client.post(reverse("poligon:exercise", args=[exercise.slug]), {"answer": "  "})
    assert page.status_code == 200
    assert "Wpisz odpowiedź po angielsku" in page.content.decode()
    assert Submission.objects.count() == 0


@pytest.mark.django_db
def test_a_choice_without_a_selection_is_rejected_on_the_server(member_client):
    exercise = make_mcq(slug="read-empty")
    page = member_client.post(reverse("poligon:exercise", args=[exercise.slug]), {})
    assert page.status_code == 200
    assert "Wybierz jedną odpowiedź" in page.content.decode()
    assert Submission.objects.count() == 0


@pytest.mark.django_db
def test_the_dashboard_names_the_next_action_and_planned_minutes(member_client):
    content = member_client.get(reverse("poligon:dashboard")).content.decode()
    assert "Co teraz" in content
    assert "Nad czym pracować" in content
    assert "Minuty z planu" in content
    assert "Plan na dziś" in content
    assert "Ostatnie ćwiczenia" in content


@pytest.mark.django_db
def test_listening_without_a_file_says_the_voice_is_synthesis(member_client):
    exercise = make_exercise(
        slug="listen-fallback",
        skill="L",
        exercise_type="listening",
        content_en="Hold at the north gate.",
        delivery={"audio_url": "", "speaker": "duty desk", "tempo": "slow", "transcript": "Hold at the north gate."},
    )
    from poligon.models import ChoiceOption

    ChoiceOption.objects.create(exercise=exercise, text_en="North gate.", text_pl="North gate.", is_correct=True)
    ChoiceOption.objects.create(exercise=exercise, text_en="South gate.", text_pl="South gate.", is_correct=False)
    content = member_client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
    assert "zapasowa synteza" in content
    assert "duty desk" in content
    assert "<audio" not in content


@pytest.mark.django_db
def test_a_real_audio_file_is_offered_when_the_exercise_has_one(member_client):
    exercise = make_exercise(
        slug="listen-file",
        skill="L",
        exercise_type="listening",
        delivery={"audio_url": "/static/poligon/audio/hold.mp3", "speaker": "duty desk", "tempo": "slow"},
    )
    content = member_client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
    assert 'src="/static/poligon/audio/hold.mp3"' in content
    assert "zapasowa synteza" not in content


@pytest.mark.django_db
def test_product_events_belong_to_the_account(member_client):
    exercise = make_mcq(slug="event-one")
    other = make_mcq(slug="event-two")
    member_client.get(reverse("poligon:exercise", args=[exercise.slug]))
    member_client.get(reverse("poligon:exercise", args=[other.slug]))
    member_client.post(
        reverse("poligon:exercise", args=[other.slug]),
        {"option_id": other.options.get(is_correct=True).pk},
    )
    names = list(ProductEvent.objects.values_list("name", flat=True))
    assert "exercise_started" in names
    assert "exercise_abandoned" in names
    assert "exercise_completed" in names


@pytest.mark.django_db
def test_a_guest_does_not_write_a_product_event(guest_client):
    exercise = make_mcq(slug="event-guest")
    guest_client.get(reverse("poligon:exercise", args=[exercise.slug]))
    assert ProductEvent.objects.count() == 0
