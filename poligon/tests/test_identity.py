import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from poligon.identity import ACCOUNT_HINT_KEY, LEVEL_KEY, SEEN_KEY
from poligon.models import LearnerState, Review, StudyEvent, Submission
from poligon.tests.conftest import PASSWORD, make_confirmed_user, pick_level, sign_in
from poligon.tests.factories import make_mcq, make_vocabulary


def answer(client, exercise, correct=True):
    option = exercise.options.get(is_correct=correct)
    return client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": option.pk})


@pytest.mark.django_db
def test_a_visit_starts_with_the_choice_of_level(client):
    landed = client.get(reverse("poligon:dashboard"))
    assert landed.status_code == 302
    assert landed.url == reverse("poligon:start")

    content = client.get(reverse("poligon:start")).content.decode()
    assert 'value="0"' not in content
    for level in range(1, 6):
        assert f'value="{level}"' in content
    assert "Wybierz, od czego zaczniesz" in content


@pytest.mark.django_db
def test_choosing_a_level_opens_the_dashboard(client):
    chosen = client.post(reverse("poligon:start"), {"practice_level": "4"})
    assert chosen.status_code == 302
    assert chosen.url == reverse("poligon:dashboard")
    assert client.session[LEVEL_KEY] == 4
    page = client.get(reverse("poligon:dashboard")).content.decode()
    assert 'class="poligon-title">4 ' in page
    assert "z 5" in page
    assert ">Start<" in page
    assert "0%" not in page
    assert "Ćwiczysz bez konta" in page


@pytest.mark.django_db
def test_a_level_outside_the_scale_is_refused(client):
    for raw in ("0", "9"):
        refused = client.post(reverse("poligon:start"), {"practice_level": raw})
        assert refused.status_code == 200
        assert "poligon-form-error" in refused.content.decode()
        assert LEVEL_KEY not in client.session


@pytest.mark.django_db
def test_a_stored_level_zero_opens_the_dashboard_at_level_one(client):
    session = client.session
    session[LEVEL_KEY] = 0
    session[SEEN_KEY] = ["old-slug"]
    session.save()

    page = client.get(reverse("poligon:dashboard"))
    assert page.status_code == 200
    assert client.session[LEVEL_KEY] == 1
    assert SEEN_KEY not in client.session
    assert 'class="poligon-title">1 ' in page.content.decode()


@pytest.mark.django_db
def test_a_signed_in_learner_skips_the_start_page(member_client):
    response = member_client.get(reverse("poligon:start"))
    assert response.status_code == 302
    assert response.url == reverse("poligon:dashboard")


@pytest.mark.django_db
def test_a_guest_leaves_nothing_behind(guest_client):
    exercise = make_mcq()
    posted = answer(guest_client, exercise)

    assert posted.status_code == 302
    assert posted.url == reverse("poligon:last_result")
    assert LearnerState.objects.count() == 0
    assert Submission.objects.count() == 0
    assert StudyEvent.objects.count() == 0
    # Only the two cookies Django itself needs to run a form.
    assert set(guest_client.cookies) <= {"sessionid", "csrftoken"}


@pytest.mark.django_db
def test_a_guest_sees_the_checked_answer_from_the_session(guest_client):
    exercise = make_mcq(explanation_pl="W notatce stoi to słowo.")
    posted = answer(guest_client, exercise, correct=False)
    content = guest_client.get(posted.url).content.decode()

    assert "Niepoprawna odpowiedź" in content
    assert "Correct choice" in content
    assert "W notatce stoi to słowo." in content


@pytest.mark.django_db
def test_the_result_page_is_empty_before_anything_is_checked(guest_client):
    response = guest_client.get(reverse("poligon:last_result"))
    assert response.status_code == 302
    assert response.url == reverse("poligon:dashboard")


@pytest.mark.django_db
def test_a_guest_hears_about_the_account_after_a_few_exercises(guest_client):
    first = guest_client.get(answer(guest_client, make_mcq(slug="one")).url).content.decode()
    assert "poligon-nudge" not in first
    guest_client.get(answer(guest_client, make_mcq(slug="two")).url)
    third = guest_client.get(answer(guest_client, make_mcq(slug="three")).url).content.decode()
    assert "poligon-nudge" in third
    assert "Zakładam konto" in third
    assert guest_client.session[ACCOUNT_HINT_KEY] is True

    again = guest_client.get(answer(guest_client, make_mcq(slug="four")).url).content.decode()
    assert "poligon-nudge" not in again


@pytest.mark.django_db
def test_a_guest_is_never_given_the_same_exercise_twice(guest_client):
    first = make_mcq(slug="read-one", skill="R")
    second = make_mcq(slug="read-two", skill="R")
    answer(guest_client, first)

    moved_on = guest_client.get(reverse("poligon:practice"), {"skill": "R"})
    assert moved_on.url == reverse("poligon:exercise", args=[second.slug])

    answer(guest_client, second)
    exhausted = guest_client.get(reverse("poligon:practice"), {"skill": "R"})
    assert exhausted.status_code == 200
    assert "To już wszystkie ćwiczenia z tej sprawności" in exhausted.content.decode()


@pytest.mark.django_db
def test_an_account_is_never_given_the_same_exercise_twice(member_client):
    first = make_mcq(slug="read-one", skill="R")
    second = make_mcq(slug="read-two", skill="R")
    answer(member_client, first)

    moved_on = member_client.get(reverse("poligon:practice"), {"skill": "R"})
    assert moved_on.url == reverse("poligon:exercise", args=[second.slug])

    answer(member_client, second)
    exhausted = member_client.get(reverse("poligon:practice"), {"skill": "R"})
    assert "Do powtórek są fiszki" in exhausted.content.decode()


@pytest.mark.django_db
def test_changing_the_level_reopens_the_whole_pool(guest_client):
    exercise = make_mcq(slug="read-one", skill="R")
    answer(guest_client, exercise)
    guest_client.post(reverse("poligon:start"), {"practice_level": "2"})

    again = guest_client.get(reverse("poligon:practice"), {"skill": "R"})
    assert again.url == reverse("poligon:exercise", args=[exercise.slug])


@pytest.mark.django_db
def test_a_fresh_account_takes_the_level_the_guest_just_picked(client):
    user = make_confirmed_user()
    client.post(reverse("poligon:start"), {"practice_level": "1"})
    signed_in = client.post(
        reverse("poligon:login"),
        {"username": user.username, "password": PASSWORD},
    )

    assert signed_in.url == reverse("poligon:dashboard")
    assert LearnerState.objects.get(user=user).practice_level == 1
    assert LEVEL_KEY not in client.session


@pytest.mark.django_db
def test_an_account_with_history_keeps_its_own_level(client):
    user = make_confirmed_user()
    account = LearnerState.objects.create(user=user, practice_level=5, target_profile="5555")
    Submission.objects.create(learner=account, exercise=make_mcq(slug="old-work"), score=90)

    client.post(reverse("poligon:start"), {"practice_level": "1"})
    sign_in(client, user)

    account.refresh_from_db()
    assert account.practice_level == 5
    assert account.target_profile == "5555"


@pytest.mark.django_db
def test_an_account_carries_its_progress_to_another_browser(client, member):
    pick_level(client)
    sign_in(client, member)
    answer(client, make_mcq())

    elsewhere = Client()
    sign_in(elsewhere, member)
    assert elsewhere.get(reverse("poligon:api_progress")).json()["submissions"] == 1


@pytest.mark.django_db
def test_two_accounts_never_see_each_other(client, member):
    sign_in(client, member)
    answer(client, make_mcq())

    other = make_confirmed_user("inny")
    theirs = Client()
    sign_in(theirs, other)
    assert theirs.get(reverse("poligon:api_progress")).json()["submissions"] == 0


@pytest.mark.django_db
def test_an_unconfirmed_account_cannot_sign_in(client):
    User.objects.create_user(username="fresh", email="fresh@example.com", password=PASSWORD)
    response = client.post(reverse("poligon:login"), {"username": "fresh", "password": PASSWORD})
    assert response.status_code == 200
    assert "Nie udało się zalogować" in response.content.decode()


@pytest.mark.django_db
def test_signing_out_leaves_the_progress_on_the_account(client, member):
    sign_in(client, member)
    answer(client, make_mcq())

    assert client.post(reverse("poligon:logout")).status_code == 302
    assert client.get(reverse("poligon:api_progress")).json()["submissions"] == 0
    assert Submission.objects.filter(learner__user=member).count() == 1


@pytest.mark.django_db
def test_flashcards_and_settings_are_for_account_holders(guest_client):
    make_vocabulary()

    cards = guest_client.get(reverse("poligon:reviews"))
    assert cards.status_code == 200
    assert "Fiszki wymagają konta" in cards.content.decode()
    assert Review.objects.count() == 0

    for name in ("settings", "placement"):
        redirected = guest_client.get(reverse(f"poligon:{name}"))
        assert redirected.status_code == 302
        assert reverse("poligon:login") in redirected.url


@pytest.mark.django_db
def test_the_account_page_explains_itself_to_a_guest(client, member):
    guest = client.get(reverse("poligon:account")).content.decode()
    assert "Ćwiczysz jako gość" in guest
    assert reverse("poligon:register") in guest

    sign_in(client, member)
    mine = client.get(reverse("poligon:account")).content.decode()
    assert member.username in mine
    assert reverse("poligon:logout") in mine
    assert reverse("poligon:export") in mine


@pytest.mark.django_db
def test_a_new_account_keeps_the_exercises_a_guest_finished(client):
    user = make_confirmed_user()
    first = make_mcq(slug="kept-one")
    second = make_mcq(slug="kept-two")
    client.post(reverse("poligon:start"), {"practice_level": "2"})
    answer(client, first)
    answer(client, second)

    sign_in(client, user)

    state = LearnerState.objects.get(user=user)
    assert set(state.submissions.values_list("exercise__slug", flat=True)) == {"kept-one", "kept-two"}
    last = state.submissions.get(exercise=second)
    assert last.score == 100
    assert last.feedback["imported_from_guest"] is True
    exhausted = client.get(reverse("poligon:practice"), {"skill": "R"})
    assert exhausted.status_code == 200
    assert "To już wszystkie ćwiczenia z tej sprawności" in exhausted.content.decode()
