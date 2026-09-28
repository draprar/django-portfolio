import pytest
from django.test import Client
from django.urls import reverse

from poligon.models import Exercise, Review, StudyEvent, Submission
from poligon.tests.factories import make_exercise, make_mcq, make_vocabulary


def test_views_facade_reexports_the_public_callables():
    from poligon import views

    assert views.dashboard is not None
    assert views.ProgressView is not None
    assert views.start is not None
    assert views.tables is not None


@pytest.mark.django_db
def test_home_redirects_to_the_dashboard(client):
    response = client.get(reverse("poligon:home"))
    assert response.status_code == 302
    assert response.url == reverse("poligon:dashboard")


@pytest.mark.django_db
def test_dashboard_is_polish_first_and_shows_a_score(member_client):
    exercise = make_mcq()
    correct = exercise.options.get(is_correct=True)
    member_client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": correct.pk})

    response = member_client.get(reverse("poligon:dashboard"))
    content = response.content.decode()
    assert response.status_code == 200
    assert 'lang="pl"' in content
    assert 'data-default-lang="pl"' in content
    assert "nie oficjalny egzamin" in content
    assert "100%" in content
    assert 'href="/#about"' not in content
    assert 'href="/gallery/"' not in content
    assert 'href="/tonguetwister/"' not in content


@pytest.mark.django_db
def test_the_header_offers_flashcards_reference_and_the_account(guest_client):
    nav = guest_client.get(reverse("poligon:dashboard")).content.decode().split("<main")[0]
    assert 'data-pl="Fiszki"' in nav
    assert 'data-pl="Tablice"' in nav
    assert reverse("poligon:login") in nav
    assert 'data-pl="Ćwicz"' not in nav
    assert reverse("poligon:settings") not in nav


@pytest.mark.django_db
def test_the_footer_keeps_the_data_page_and_drops_the_hub(guest_client):
    footer = guest_client.get(reverse("poligon:dashboard")).content.decode().split("</main>")[1]
    assert reverse("poligon:policy") in footer
    assert reverse("poligon:settings") not in footer
    assert "/wybierz/" not in footer


@pytest.mark.django_db
def test_settings_reach_the_footer_once_there_is_an_account(member_client):
    footer = member_client.get(reverse("poligon:dashboard")).content.decode().split("</main>")[1]
    assert reverse("poligon:settings") in footer


@pytest.mark.django_db
def test_dashboard_sends_each_skill_card_to_its_own_queue(guest_client):
    content = guest_client.get(reverse("poligon:dashboard")).content.decode()
    for skill in ("L", "S", "R", "W"):
        assert f'{reverse("poligon:practice")}?skill={skill}' in content
    assert reverse("poligon:api_progress") not in content


@pytest.mark.django_db
def test_dashboard_counts_due_cards_in_the_header_badge(member_client):
    make_vocabulary()
    member_client.get(reverse("poligon:reviews"))
    content = member_client.get(reverse("poligon:dashboard")).content.decode()
    assert "poligon-badge" in content


@pytest.mark.django_db
def test_practice_opens_the_first_active_exercise_for_a_skill(guest_client):
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

    response = guest_client.get(reverse("poligon:practice"), {"skill": "W"})
    assert response.status_code == 302
    assert response.url == reverse("poligon:exercise", args=[writing.slug])


@pytest.mark.django_db
def test_practice_stays_on_the_selected_level(guest_client):
    make_mcq(slug="read-level-2", skill="R", level=2)
    harder = make_mcq(slug="read-level-3", skill="R", level=3)
    guest_client.post(reverse("poligon:start"), {"practice_level": "3"})

    response = guest_client.get(reverse("poligon:practice"), {"skill": "R"})
    assert response.status_code == 302
    assert response.url == reverse("poligon:exercise", args=[harder.slug])


@pytest.mark.django_db
def test_empty_state_talks_to_the_learner_not_the_admin(guest_client):
    response = guest_client.get(reverse("poligon:practice"), {"skill": "W"})
    content = response.content.decode()
    assert response.status_code == 200
    assert "poligon-empty" in content
    assert "Pisanie" in content
    assert "admin" not in content
    assert reverse("poligon:start") in content


@pytest.mark.django_db
def test_mcq_submission_redirects_to_its_own_result_page(member_client):
    exercise = make_mcq()
    wrong = exercise.options.get(is_correct=False)
    posted = member_client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": wrong.pk})

    submission = Submission.objects.get()
    assert posted.status_code == 302
    assert posted.url == reverse("poligon:result", args=[submission.pk])
    assert submission.score == 0
    assert StudyEvent.objects.get().minutes == exercise.expected_minutes

    content = member_client.get(posted.url).content.decode()
    assert "0%" in content
    assert "Tym razem nie" in content
    assert "Correct choice" in content
    assert "<form" not in content
    # The way on from here is the dashboard, and it comes first.
    actions = content.split("poligon-actions")[1].split("</div>")[0]
    assert actions.index("Wróć na pulpit") < actions.index("Jeszcze jedno takie")


@pytest.mark.django_db
def test_a_wrong_choice_explains_itself_when_the_item_says_why(member_client):
    exercise = make_mcq(
        slug="read-why",
        explanation_pl="W notatce stoi to słowo.",
        explanation_en="The note says that word.",
    )
    posted = member_client.post(
        reverse("poligon:exercise", args=[exercise.slug]),
        {"option_id": exercise.options.get(is_correct=False).pk},
    )
    content = member_client.get(posted.url).content.decode()
    assert "W notatce stoi to słowo." in content
    assert 'data-en="The note says that word."' in content


@pytest.mark.django_db
def test_a_right_choice_does_not_explain_anything(member_client):
    exercise = make_mcq(slug="read-quiet", explanation_pl="W notatce stoi to słowo.")
    posted = member_client.post(
        reverse("poligon:exercise", args=[exercise.slug]),
        {"option_id": exercise.options.get(is_correct=True).pk},
    )
    content = member_client.get(posted.url).content.decode()
    assert "Dobrze" in content
    assert "W notatce stoi to słowo." not in content


@pytest.mark.django_db
def test_a_short_answer_is_told_what_to_do_next(member_client):
    exercise = make_exercise(slug="write-short", skill="W", exercise_type="writing")
    posted = member_client.post(reverse("poligon:exercise", args=[exercise.slug]), {"answer": "Water."})
    content = member_client.get(posted.url).content.decode()
    assert "To za krótko" in content


@pytest.mark.django_db
def test_a_result_page_belongs_to_one_learner_only(member_client):
    exercise = make_mcq()
    correct = exercise.options.get(is_correct=True)
    posted = member_client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": correct.pk})

    assert member_client.get(posted.url).status_code == 200
    assert Client().get(posted.url).status_code == 404


@pytest.mark.django_db
def test_writing_result_shows_the_heuristic_as_a_hint(member_client):
    exercise = make_exercise(slug="write", skill="W", exercise_type="writing")
    posted = member_client.post(
        reverse("poligon:exercise", args=[exercise.slug]),
        {"answer": "First we move to the site. Then we check the equipment."},
    )
    assert posted.status_code == 302
    content = member_client.get(posted.url).content.decode()
    assert "nie oficjalna ocena" in content
    assert "Budowa zdań" in content
    assert Submission.objects.get().score > 0


@pytest.mark.django_db
def test_a_writing_task_offers_the_polish_translation_on_request(guest_client):
    exercise = make_exercise(slug="write-pl", skill="W", exercise_type="writing")
    content = guest_client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
    assert exercise.prompt_en in content
    assert exercise.get_prompt("pl") in content
    assert "poligon-reveal" in content
    assert 'for="poligon-answer"' in content


@pytest.mark.django_db
def test_answer_choices_are_never_translated_into_polish(guest_client):
    exercise = make_mcq(slug="read-en-only")
    content = guest_client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
    assert "Correct choice" in content
    assert "Poprawna" not in content


@pytest.mark.django_db
def test_the_right_answer_does_not_always_come_first(guest_client):
    """Twenty questions in a row all answered "a" would teach the wrong habit."""
    first_is_correct = 0
    for index in range(20):
        exercise = make_mcq(slug=f"shuffle-{index}")
        content = guest_client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
        options = content.split('class="poligon-option"')[1:]
        correct_id = str(exercise.options.get(is_correct=True).pk)
        if f'value="{correct_id}"' in options[0]:
            first_is_correct += 1
    assert 0 < first_is_correct < 20


@pytest.mark.django_db
def test_the_options_keep_their_order_when_the_page_is_reloaded(guest_client):
    exercise = make_mcq(slug="stable")
    url = reverse("poligon:exercise", args=[exercise.slug])

    def order(response):
        return [chunk.split('"')[0] for chunk in response.content.decode().split('name="option_id" value="')[1:]]

    assert len(order(guest_client.get(url))) == 2
    assert order(guest_client.get(url)) == order(guest_client.get(url))


@pytest.mark.django_db
def test_a_listening_script_is_spoken_in_english_and_hidden_by_default(guest_client):
    exercise = make_mcq(
        slug="listen-one",
        skill="L",
        exercise_type="listening",
        content_en="Confirm the water before the team starts.",
        content_pl="Potwierdź wodę, zanim zespół zacznie.",
    )
    content = guest_client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
    assert 'data-pl="Pokaż tekst"' in content
    assert exercise.content_en in content
    assert exercise.content_pl not in content
    assert '"en-US"' in content


@pytest.mark.django_db
def test_inactive_exercise_is_not_served(guest_client):
    exercise = make_mcq(active=False)
    response = guest_client.get(reverse("poligon:exercise", args=[exercise.slug]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_reviews_and_grade_update_the_schedule(member_client):
    make_vocabulary()
    page = member_client.get(reverse("poligon:reviews"))
    content = page.content.decode()
    assert page.status_code == 200
    assert "briefing" in content
    assert "Pamiętam" in content
    assert "1, 2, 3, 4" in content
    review = Review.objects.get()

    graded = member_client.post(reverse("poligon:grade_review", args=[review.pk]), {"grade": "4"})
    assert graded.status_code == 302
    review.refresh_from_db()
    assert review.last_grade == 4
    assert review.repetitions == 1

    ignored = member_client.post(reverse("poligon:grade_review", args=[review.pk]), {"grade": "nope"})
    assert ignored.status_code == 302
    review.refresh_from_db()
    assert review.last_grade == 4


@pytest.mark.django_db
def test_reviews_page_when_nothing_is_due(member_client):
    response = member_client.get(reverse("poligon:reviews"))
    assert response.status_code == 200
    content = response.content.decode()
    assert "poligon-caught-up" in content
    assert reverse("poligon:dashboard") in content


@pytest.mark.django_db
def test_settings_save_and_reject_bad_input(member_client):
    saved = member_client.post(
        reverse("poligon:settings"),
        {"practice_level": "3", "daily_minutes": "40", "target_date": "2026-12-01"},
    )
    assert saved.status_code == 302
    from poligon.models import LearnerState

    state = LearnerState.objects.get()
    assert state.practice_level == 3
    assert state.target_profile == "3333"
    state_page = member_client.get(reverse("poligon:dashboard"))
    assert '<h1 class="poligon-title">3</h1>' in state_page.content.decode()

    for bad in (
        {"practice_level": "9", "daily_minutes": "35", "target_date": ""},
        {"practice_level": "2", "daily_minutes": "soon", "target_date": ""},
        {"practice_level": "2", "daily_minutes": "35", "target_date": "yesterday"},
        {"practice_level": "2", "daily_minutes": "9", "target_date": ""},
    ):
        response = member_client.post(reverse("poligon:settings"), bad)
        assert response.status_code == 200
        assert "poligon-form-error" in response.content.decode()


@pytest.mark.django_db
def test_settings_can_clear_the_target_date(member_client):
    member_client.post(
        reverse("poligon:settings"),
        {"practice_level": "1", "daily_minutes": "35", "target_date": "2026-12-01"},
    )
    cleared = member_client.post(
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
def test_the_reference_tab_is_a_cheat_sheet_and_not_a_test(guest_client):
    response = guest_client.get(reverse("poligon:tables"))
    content = response.content.decode()
    assert response.status_code == 200
    assert "Alpha" in content
    assert "Zulu" in content
    assert "Could you spell that, please?" in content
    assert "na łączność, w terenie i na odprawę" in content
    assert "<form" not in content
    assert "STANAG" not in content
    assert "NATO" not in content


@pytest.mark.django_db
def test_the_data_page_lists_every_cookie_we_set(guest_client):
    response = guest_client.get(reverse("poligon:policy"))
    content = response.content.decode()
    assert response.status_code == 200
    for name in ("sessionid", "csrftoken", "site_lang"):
        assert name in content
    assert "niezbędne" in content
    assert "Nagranie nie opuszcza urządzenia" in content


@pytest.mark.django_db
def test_the_sources_page_is_gone():
    from django.urls import NoReverseMatch

    with pytest.raises(NoReverseMatch):
        reverse("poligon:sources")


@pytest.mark.django_db
def test_a_borrowed_passage_links_the_article_and_the_license(guest_client):
    exercise = make_mcq(
        content_source="wikipedia",
        source_url="https://en.wikipedia.org/wiki/Weather",
        source_license="CC BY-SA 4.0",
        attribution_en="Shortened English text from the Wikipedia article Weather, CC BY-SA 4.0.",
        attribution_pl="Skrócony angielski tekst z artykułu Wikipedii Weather, CC BY-SA 4.0.",
    )
    content = guest_client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
    assert 'href="https://en.wikipedia.org/wiki/Weather"' in content
    assert 'href="https://creativecommons.org/licenses/by-sa/4.0/"' in content


@pytest.mark.django_db
def test_a_flashcard_links_the_tatoeba_sentence_as_well_as_the_definition(member_client):
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
    content = member_client.get(reverse("poligon:reviews")).content.decode()
    assert 'href="https://en.wiktionary.org/wiki/water"' in content
    assert 'href="https://creativecommons.org/licenses/by-sa/4.0/"' in content
    assert 'href="https://creativecommons.org/licenses/by/2.0/fr/"' in content
    assert 'href="https://tatoeba.org/en/sentences/show/6289899"' in content


@pytest.mark.django_db
def test_a_listening_task_says_it_is_not_a_voice_recording(guest_client):
    exercise = make_mcq(slug="listen-honest", skill="L", exercise_type="listening", content_en="Water.")
    content = guest_client.get(reverse("poligon:exercise", args=[exercise.slug])).content.decode()
    assert "nie nagranie lektora" in content


@pytest.mark.django_db
def test_a_speaking_task_says_the_grade_is_not_official(member_client):
    exercise = make_exercise(slug="speak-honest", skill="S", exercise_type="speaking")
    posted = member_client.post(
        reverse("poligon:exercise", args=[exercise.slug]),
        {"answer": "We move at first light and confirm the route on arrival."},
    )
    assert "nie oficjalna ocena" in member_client.get(posted.url).content.decode()
