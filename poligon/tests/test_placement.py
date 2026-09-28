import pytest
from django.urls import reverse

from poligon.models import LearnerState, Submission
from poligon.tests.factories import make_mcq


def build_quiz():
    """Two reading questions per level, the way placement picks them."""
    questions = []
    for level in (1, 2, 3, 4, 5):
        for index in range(2):
            questions.append(make_mcq(slug=f"p-{level}-{index}", skill="R", level=level))
    return questions


def answers(questions, right_count):
    posted = {}
    for position, question in enumerate(questions):
        option = question.options.get(is_correct=position < right_count)
        posted[f"q{question.pk}"] = option.pk
    return posted


@pytest.mark.django_db
def test_placement_asks_ten_questions_in_english(member_client):
    build_quiz()
    content = member_client.get(reverse("poligon:placement")).content.decode()
    assert "10/10" in content
    assert "Question in English." in content
    assert "Pytanie po polsku." not in content


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("right", "expected"),
    [(0, 0), (1, 0), (2, 1), (5, 2), (8, 4), (10, 5)],
)
def test_two_right_answers_are_worth_one_level(member_client, right, expected):
    questions = build_quiz()
    response = member_client.post(reverse("poligon:placement"), answers(questions, right))
    content = response.content.decode()
    assert response.status_code == 200
    assert f'<h1 class="poligon-title">{expected}</h1>' in content
    assert f"{right} z 10 dobrze" in content


@pytest.mark.django_db
def test_placement_is_a_suggestion_until_the_learner_accepts_it(member_client):
    questions = build_quiz()
    member_client.post(reverse("poligon:placement"), answers(questions, 8))
    assert LearnerState.objects.get().practice_level == 2

    applied = member_client.post(
        reverse("poligon:settings"),
        {"practice_level": "4", "daily_minutes": "35", "target_date": ""},
    )
    assert applied.status_code == 302
    assert LearnerState.objects.get().practice_level == 4


@pytest.mark.django_db
def test_placement_does_not_count_as_practice(member_client):
    questions = build_quiz()
    member_client.post(reverse("poligon:placement"), answers(questions, 10))
    assert Submission.objects.count() == 0


@pytest.mark.django_db
def test_placement_without_a_catalog_falls_back_to_the_empty_state(member_client):
    response = member_client.get(reverse("poligon:placement"))
    assert response.status_code == 200
    assert "poligon-empty" in response.content.decode()


@pytest.mark.django_db
def test_a_new_account_is_offered_the_level_check(member_client):
    make_mcq()
    fresh = member_client.get(reverse("poligon:dashboard")).content.decode()
    assert reverse("poligon:placement") in fresh

    exercise = make_mcq(slug="done-one")
    member_client.post(
        reverse("poligon:exercise", args=[exercise.slug]),
        {"option_id": exercise.options.get(is_correct=True).pk},
    )
    busy = member_client.get(reverse("poligon:dashboard")).content.decode()
    assert "Pierwszy raz tutaj?" not in busy


@pytest.mark.django_db
def test_a_guest_is_not_offered_the_level_check(guest_client):
    make_mcq()
    content = guest_client.get(reverse("poligon:dashboard")).content.decode()
    assert reverse("poligon:placement") not in content
