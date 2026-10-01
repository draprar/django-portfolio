import pytest
from django.core.management import call_command
from django.urls import reverse

from poligon.models import Exercise, LearnerState, PlacementAttempt, Submission
from poligon.tests.factories import make_mcq


def load_bank():
    call_command("seed_poligon", "--placement-only")
    return list(Exercise.objects.filter(catalog_role="placement").order_by("level", "slug"))


def answers(questions, right_count):
    posted = {}
    for position, question in enumerate(questions):
        if position < right_count:
            option = question.options.get(is_correct=True)
        else:
            option = question.options.filter(is_correct=False).first()
        posted[f"q{question.pk}"] = option.pk
    return posted


@pytest.mark.django_db
def test_placement_asks_fifteen_questions_from_the_bank(member_client):
    load_bank()
    make_mcq(slug="practice-note", prompt_en="This practice item is not a placement question.")
    content = member_client.get(reverse("poligon:placement")).content.decode()
    assert "Pytanie 1 z 15" in content
    assert "STANAG" not in content
    assert "The vehicle gate opens at seven thirty." in content
    assert "This practice item is not a placement question." not in content
    assert "Pytanie po polsku." not in content


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("right", "expected"),
    [(0, 1), (3, 1), (4, 2), (6, 2), (7, 3), (9, 3), (10, 4), (12, 4), (13, 5), (15, 5)],
)
def test_placement_v1_suggests_a_level_from_fifteen_answers(member_client, right, expected):
    questions = load_bank()
    response = member_client.post(reverse("poligon:placement"), answers(questions, right))
    content = response.content.decode()
    assert response.status_code == 200
    assert f'<h1 class="poligon-title">{expected}</h1>' in content
    assert f"proponujemy poziom {expected}" in content
    assert "oficjalna ocena" in content
    assert "Twój angielski to poziom" not in content
    attempt = PlacementAttempt.objects.get()
    assert attempt.algorithm_version == "placement_v1"
    assert attempt.correct_count == right
    assert attempt.suggested_level == expected
    assert attempt.question_count == 15


@pytest.mark.django_db
def test_placement_is_a_suggestion_until_the_learner_accepts_it(member_client):
    questions = load_bank()
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
    questions = load_bank()
    member_client.post(reverse("poligon:placement"), answers(questions, 10))
    assert Submission.objects.count() == 0


@pytest.mark.django_db
def test_placement_does_not_always_lead_with_the_right_answer(member_client):
    questions = load_bank()
    content = member_client.get(reverse("poligon:placement")).content.decode()
    first_is_correct = 0
    for question in questions:
        correct_id = str(question.options.get(is_correct=True).pk)
        marker = f'name="q{question.pk}" value="'
        first = content.split(marker)[1].split('"')[0]
        if first == correct_id:
            first_is_correct += 1
    assert 0 < first_is_correct < len(questions)


@pytest.mark.django_db
def test_placement_ignores_the_practice_catalog(member_client):
    load_bank()
    make_mcq(slug="wiki-easy", level=1, content_source="wikipedia", prompt_en="A long Wikipedia lead about logistics.")
    make_mcq(slug="note-a", level=1, content_source="original", prompt_en="The gate opens at seven.")
    content = member_client.get(reverse("poligon:placement")).content.decode()
    assert "The vehicle gate opens at seven thirty." in content
    assert "The gate opens at seven." not in content
    assert "A long Wikipedia lead about logistics." not in content


@pytest.mark.django_db
def test_placement_is_empty_when_only_a_wikipedia_lead_exists(member_client):
    lead = "Weather changes every hour. " + ("Storms follow the coast. " * 40)
    make_mcq(slug="wiki-only", level=1, content_source="wikipedia", prompt_en=lead)
    content = member_client.get(reverse("poligon:placement")).content.decode()
    assert "poligon-empty" in content
    assert "Weather changes every hour." not in content


@pytest.mark.django_db
def test_placement_skips_an_inactive_gist_and_a_wikipedia_item(member_client):
    load_bank()
    make_mcq(slug="gist-off", level=2, active=False, prompt_en="It is about the water.")
    make_mcq(
        slug="wiki-on",
        level=2,
        content_source="wikipedia",
        prompt_en="A Wikipedia lead about a bridge.",
    )
    content = member_client.get(reverse("poligon:placement")).content.decode()
    assert "The vehicle gate opens at seven thirty." in content
    assert "It is about the water." not in content
    assert "A Wikipedia lead about a bridge." not in content


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
    assert "średnia trafność" in fresh
    assert "0%" in fresh

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
