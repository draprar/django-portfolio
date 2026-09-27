import pytest
from django.test import Client
from django.urls import reverse

from poligon.models import Exercise, Review, StudyEvent, Submission
from poligon.tests.factories import make_exercise, make_mcq, make_vocabulary


def test_views_facade_reexports_the_public_callables():
    from poligon import views

    assert views.dashboard is not None
    assert views.ProgressView is not None


@pytest.mark.django_db
def test_home_redirects_to_the_dashboard(client):
    response = client.get(reverse("poligon:home"))
    assert response.status_code == 302
    assert response.url == reverse("poligon:dashboard")


@pytest.mark.django_db
def test_dashboard_is_polish_first_and_shows_a_score(client):
    exercise = make_mcq()
    correct = exercise.options.get(is_correct=True)
    client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": correct.pk})

    response = client.get(reverse("poligon:dashboard"))
    content = response.content.decode()
    assert response.status_code == 200
    assert 'lang="pl"' in content
    assert 'data-default-lang="pl"' in content
    assert "to nie egzamin" in content
    assert "100%" in content
    assert 'href="/#about"' not in content
    assert 'href="/gallery/"' not in content
    assert 'href="/tonguetwister/"' not in content


@pytest.mark.django_db
def test_header_keeps_only_the_two_learning_destinations(client):
    response = client.get(reverse("poligon:dashboard"))
    nav = response.content.decode().split("<main")[0]
    assert 'data-pl="Ćwicz"' in nav
    assert 'data-pl="Fiszki"' in nav
    assert reverse("poligon:settings") not in nav
    assert reverse("poligon:sources") not in nav


@pytest.mark.django_db
def test_settings_and_sources_stay_reachable_from_the_footer(client):
    footer = client.get(reverse("poligon:dashboard")).content.decode().split("</main>")[1]
    assert reverse("poligon:settings") in footer
    assert reverse("poligon:sources") in footer
    assert "/wybierz/" in footer


@pytest.mark.django_db
def test_dashboard_sends_each_skill_card_to_its_own_queue(client):
    content = client.get(reverse("poligon:dashboard")).content.decode()
    for skill in ("L", "S", "R", "W"):
        assert f'{reverse("poligon:practice")}?skill={skill}' in content
    assert reverse("poligon:api_progress") not in content


@pytest.mark.django_db
def test_dashboard_counts_due_cards_in_the_header_badge(client):
    make_vocabulary()
    client.get(reverse("poligon:reviews"))
    content = client.get(reverse("poligon:dashboard")).content.decode()
    assert "poligon-badge" in content


@pytest.mark.django_db
def test_practice_opens_the_first_active_exercise_for_a_skill(client):
    make_mcq(slug="read-one", skill="R")
    writing = make_exercise(slug="write-one", skill="W", exercise_type="writing")
    Exercise.objects.create(
        slug="hidden",
        title_pl="Ukryte",
        title_en="Hidden",
        skill="W",
        exercise_type="writing",
        instructions_pl="x",
        instructions_en="x",
        prompt_pl="x",
        prompt_en="x",
        active=False,
    )

    response = client.get(reverse("poligon:practice"), {"skill": "W"})
    assert response.status_code == 302
    assert response.url == reverse("poligon:exercise", args=[writing.slug])


@pytest.mark.django_db
def test_practice_stays_on_the_selected_level(client):
    make_mcq(slug="read-level-2", skill="R", level=2)
    harder = make_mcq(slug="read-level-3", skill="R", level=3)
    client.post(
        reverse("poligon:settings"),
        {"practice_level": "3", "daily_minutes": "35", "target_date": ""},
    )
    response = client.get(reverse("poligon:practice"), {"skill": "R"})
    assert response.status_code == 302
    assert response.url == reverse("poligon:exercise", args=[harder.slug])


@pytest.mark.django_db
def test_practice_skips_an_exercise_already_done_this_session(client):
    done = make_mcq(slug="read-done", skill="R")
    pending = make_mcq(slug="read-next", skill="R")
    correct = done.options.get(is_correct=True)
    client.post(reverse("poligon:exercise", args=[done.slug]), {"option_id": correct.pk})

    response = client.get(reverse("poligon:practice"), {"skill": "R"})
    assert response.status_code == 302
    assert response.url == reverse("poligon:exercise", args=[pending.slug])


@pytest.mark.django_db
def test_empty_state_talks_to_the_learner_not_the_admin(client):
    response = client.get(reverse("poligon:practice"), {"skill": "W"})
    content = response.content.decode()
    assert response.status_code == 200
    assert "poligon-empty" in content
    assert "Pisanie" in content
    assert "admin" not in content
    assert reverse("poligon:settings") in content


@pytest.mark.django_db
def test_mcq_submission_redirects_to_its_own_result_page(client):
    exercise = make_mcq()
    wrong = exercise.options.get(is_correct=False)
    posted = client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": wrong.pk})

    submission = Submission.objects.get()
    assert posted.status_code == 302
    assert posted.url == reverse("poligon:result", args=[submission.pk])
    assert submission.score == 0
    assert StudyEvent.objects.get().minutes == exercise.expected_minutes

    content = client.get(posted.url).content.decode()
    assert "0%" in content
    assert "Tym razem nie" in content
    assert "Correct choice" in content
    assert "<form" not in content


@pytest.mark.django_db
def test_a_wrong_choice_explains_itself_when_the_item_says_why(client):
    exercise = make_mcq(
        slug="read-why",
        explanation_pl="W notatce stoi to słowo.",
        explanation_en="The note says that word.",
    )
    posted = client.post(
        reverse("poligon:exercise", args=[exercise.slug]),
        {"option_id": exercise.options.get(is_correct=False).pk},
    )
    content = client.get(posted.url).content.decode()
    assert "W notatce stoi to słowo." in content
    assert 'data-en="The note says that word."' in content


@pytest.mark.django_db
def test_a_right_choice_does_not_explain_anything(client):
    exercise = make_mcq(slug="read-quiet", explanation_pl="W notatce stoi to słowo.")
    posted = client.post(
        reverse("poligon:exercise", args=[exercise.slug]),
        {"option_id": exercise.options.get(is_correct=True).pk},
    )
    content = client.get(posted.url).content.decode()
    assert "Dobrze" in content
    assert "W notatce stoi to słowo." not in content


@pytest.mark.django_db
def test_a_short_answer_is_told_what_to_do_next(client):
    exercise = make_exercise(slug="write-short", skill="W", exercise_type="writing")
    posted = client.post(reverse("poligon:exercise", args=[exercise.slug]), {"answer": "Water."})
    content = client.get(posted.url).content.decode()
    assert "To za krótko" in content


@pytest.mark.django_db
def test_a_result_page_belongs_to_one_learner_only(client):
    exercise = make_mcq()
    correct = exercise.options.get(is_correct=True)
    posted = client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": correct.pk})

    assert client.get(posted.url).status_code == 200
    assert Client().get(posted.url).status_code == 404


@pytest.mark.django_db
def test_writing_result_shows_the_heuristic_as_a_hint(client):
    exercise = make_exercise(slug="write", skill="W", exercise_type="writing")
    posted = client.post(
        reverse("poligon:exercise", args=[exercise.slug]),
        {"answer": "First we move to the site. Then we check the equipment."},
    )
    assert posted.status_code == 302
    content = client.get(posted.url).content.decode()
    assert "nie ocena z egzaminu" in content
    assert "Budowa zdań" in content
    assert Submission.objects.get().score > 0


@pytest.mark.django_db
def test_a_writing_task_offers_the_polish_translation_on_request(client):
    exercise = make_exercise(slug="write-pl", skill="W", exercise_type="writing")
    content = client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
    assert exercise.prompt_en in content
    assert exercise.get_prompt("pl") in content
    assert "poligon-reveal" in content
    assert 'for="poligon-answer"' in content


@pytest.mark.django_db
def test_answer_choices_are_never_translated_into_polish(client):
    exercise = make_mcq(slug="read-en-only")
    content = client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
    assert "Correct choice" in content
    assert "Poprawna" not in content


@pytest.mark.django_db
def test_a_listening_script_is_spoken_in_english_and_hidden_by_default(client):
    exercise = make_mcq(
        slug="listen-one",
        skill="L",
        exercise_type="listening",
        content_en="Confirm the water before the team starts.",
        content_pl="Potwierdź wodę, zanim zespół zacznie.",
    )
    content = client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
    assert 'data-pl="Pokaż tekst"' in content
    assert exercise.content_en in content
    assert exercise.content_pl not in content
    assert '"en-US"' in content


@pytest.mark.django_db
def test_inactive_exercise_is_not_served(client):
    exercise = make_mcq(active=False)
    response = client.get(reverse("poligon:exercise", args=[exercise.slug]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_reviews_and_grade_update_the_schedule(client):
    make_vocabulary()
    page = client.get(reverse("poligon:reviews"))
    content = page.content.decode()
    assert page.status_code == 200
    assert "briefing" in content
    assert "Pamiętam" in content
    assert "1, 2, 3, 4" in content
    review = Review.objects.get()

    graded = client.post(reverse("poligon:grade_review", args=[review.pk]), {"grade": "4"})
    assert graded.status_code == 302
    review.refresh_from_db()
    assert review.last_grade == 4
    assert review.repetitions == 1

    ignored = client.post(reverse("poligon:grade_review", args=[review.pk]), {"grade": "nope"})
    assert ignored.status_code == 302
    review.refresh_from_db()
    assert review.last_grade == 4


@pytest.mark.django_db
def test_reviews_page_when_nothing_is_due(client):
    response = client.get(reverse("poligon:reviews"))
    assert response.status_code == 200
    assert "poligon-caught-up" in response.content.decode()


@pytest.mark.django_db
def test_settings_save_and_reject_bad_input(client):
    saved = client.post(
        reverse("poligon:settings"),
        {"practice_level": "3", "daily_minutes": "40", "target_date": "2026-12-01"},
    )
    assert saved.status_code == 302
    from poligon.models import LearnerState

    state = LearnerState.objects.get()
    assert state.practice_level == 3
    assert state.target_profile == "3333"
    state_page = client.get(reverse("poligon:dashboard"))
    assert '<h1 class="poligon-title">3</h1>' in state_page.content.decode()

    bad_level = client.post(
        reverse("poligon:settings"),
        {"practice_level": "9", "daily_minutes": "35", "target_date": ""},
    )
    assert bad_level.status_code == 200
    assert "poligon-form-error" in bad_level.content.decode()

    bad_minutes = client.post(
        reverse("poligon:settings"),
        {"practice_level": "2", "daily_minutes": "soon", "target_date": ""},
    )
    assert bad_minutes.status_code == 200
    assert "poligon-form-error" in bad_minutes.content.decode()

    bad_date = client.post(
        reverse("poligon:settings"),
        {"practice_level": "2", "daily_minutes": "35", "target_date": "yesterday"},
    )
    assert bad_date.status_code == 200
    assert "poligon-form-error" in bad_date.content.decode()

    out_of_range = client.post(
        reverse("poligon:settings"),
        {"practice_level": "2", "daily_minutes": "9", "target_date": ""},
    )
    assert out_of_range.status_code == 200


@pytest.mark.django_db
def test_settings_can_clear_the_target_date(client):
    client.post(
        reverse("poligon:settings"),
        {"practice_level": "1", "daily_minutes": "35", "target_date": "2026-12-01"},
    )
    cleared = client.post(
        reverse("poligon:settings"),
        {"practice_level": "1", "daily_minutes": "35", "target_date": ""},
    )
    assert cleared.status_code == 302
    from poligon.models import LearnerState

    state = LearnerState.objects.get()
    assert state.target_date is None
    assert state.practice_level == 1
    assert state.target_profile == "1111"


@pytest.mark.django_db
def test_sources_page_names_the_provenance_rules(client):
    response = client.get(reverse("poligon:sources"))
    content = response.content.decode()
    assert response.status_code == 200
    assert "Original Ćwiczba exercises" in content
    assert "Wiktionary" in content
    assert "Wikipedia" in content
    assert "Tatoeba" in content
    assert "CC BY-SA" in content
    assert "nie jest oficjalny wynik" in content
    assert "data-pl=" in content


@pytest.mark.django_db
def test_a_borrowed_passage_links_the_article_and_the_license(client):
    exercise = make_mcq(
        content_source="wikipedia",
        source_url="https://en.wikipedia.org/wiki/Weather",
        source_license="CC BY-SA 4.0",
        attribution_en="Shortened English text from the Wikipedia article Weather, CC BY-SA 4.0.",
        attribution_pl="Skrócony angielski tekst z artykułu Wikipedii Weather, CC BY-SA 4.0.",
    )
    content = client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
    assert 'href="https://en.wikipedia.org/wiki/Weather"' in content
    assert 'href="https://creativecommons.org/licenses/by-sa/4.0/"' in content


@pytest.mark.django_db
def test_a_flashcard_links_the_tatoeba_sentence_as_well_as_the_definition(client):
    make_vocabulary(
        content_source="wiktionary",
        source_url="https://en.wiktionary.org/wiki/water",
        source_license="CC BY-SA 4.0",
        attribution_en=(
            "English definition from Wiktionary contributors, CC BY-SA 4.0. "
            "Example from Tatoeba #6289899 by megamanenm, CC BY 2.0 FR."
        ),
        attribution_pl=(
            "Angielska definicja: współtwórcy Wiktionary, CC BY-SA 4.0. "
            "Przykład z Tatoeby #6289899, autor: megamanenm, CC BY 2.0 FR."
        ),
    )
    content = client.get(reverse("poligon:reviews")).content.decode()
    assert 'href="https://en.wiktionary.org/wiki/water"' in content
    assert 'href="https://creativecommons.org/licenses/by-sa/4.0/"' in content
    assert 'href="https://creativecommons.org/licenses/by/2.0/fr/"' in content
    assert 'href="https://tatoeba.org/en/sentences/show/6289899"' in content


@pytest.mark.django_db
def test_sources_page_admits_what_is_still_a_stand_in(client):
    content = client.get(reverse("poligon:sources")).content.decode()
    assert "nie nagranie lektora" in content
    assert "nie jest oceniane" in content
