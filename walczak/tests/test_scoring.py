import pytest
from django.core.exceptions import ValidationError

from walczak.models import Choice, Question, Style
from walczak.scoring import choose_style


def make_style(**kwargs) -> Style:
    defaults = {
        "slug": "test-styl",
        "name_pl": "Test",
        "name_en": "Test",
        "family": "uderzenia",
        "joke_pl": "Żart.",
        "joke_en": "A joke.",
        "summary_pl": "Opis.",
        "summary_en": "A summary.",
        "sort_order": 100,
        "active": True,
    }
    defaults.update(kwargs)
    return Style.objects.create(**defaults)


@pytest.mark.django_db
def test_blank_answers_pick_the_first_active_style():
    winner = choose_style([], {})

    assert winner is not None
    assert winner.slug == "boks"


@pytest.mark.django_db
def test_higher_points_beat_the_extra_style():
    quiet = make_style(slug="cichy", name_pl="Cichy", sort_order=50)
    loud = make_style(slug="glosny", name_pl="Głośny", sort_order=51)
    question = Question.objects.create(text_pl="Pytanie", text_en="Question", sort_order=50)
    choice = Choice.objects.create(
        question=question,
        text_pl="Odpowiedź",
        text_en="Answer",
        sort_order=1,
        style=loud,
        points=3,
        extra_style=quiet,
        extra_points=1,
    )

    winner = choose_style([question], {f"q{question.pk}": str(choice.pk)})

    assert winner is not None
    assert winner.slug == "glosny"


@pytest.mark.django_db
def test_unknown_choice_does_not_crash():
    question = Question.objects.create(text_pl="Pytanie", text_en="Question", sort_order=60)

    winner = choose_style([question], {f"q{question.pk}": "999999"})

    assert winner is not None
    assert winner.slug == "boks"


@pytest.mark.django_db
def test_no_active_style_returns_nothing():
    Style.objects.update(active=False)

    assert choose_style([], {}) is None


@pytest.mark.django_db
def test_choice_without_an_extra_style_drops_the_points():
    style = Style.objects.get(slug="boks")
    question = Question.objects.create(text_pl="Pytanie", text_en="Question", sort_order=81)
    choice = Choice(
        question=question,
        text_pl="Sam",
        text_en="Alone",
        style=style,
        points=1,
        extra_points=4,
        sort_order=1,
    )

    choice.full_clean()

    assert choice.extra_points == 0


@pytest.mark.django_db
def test_tie_goes_to_the_lower_sort_order():
    make_style(slug="wczesny", name_pl="Wczesny", sort_order=0)
    question = Question.objects.create(text_pl="Pytanie", text_en="Question", sort_order=70)
    left = make_style(slug="lewy", name_pl="Lewy", sort_order=20)
    right = make_style(slug="prawy", name_pl="Prawy", sort_order=21)
    choice_left = Choice.objects.create(
        question=question,
        text_pl="Lewo",
        text_en="Left",
        style=left,
        points=2,
        sort_order=1,
    )
    Choice.objects.create(
        question=question,
        text_pl="Prawo",
        text_en="Right",
        style=right,
        points=2,
        sort_order=2,
    )
    other = Question.objects.create(text_pl="Drugie", text_en="Second", sort_order=71)
    Choice.objects.create(
        question=other,
        text_pl="Znowu lewo",
        text_en="Left again",
        style=left,
        points=2,
        sort_order=1,
    )
    choice_right = Choice.objects.create(
        question=other,
        text_pl="Znowu prawo",
        text_en="Right again",
        style=right,
        points=2,
        sort_order=2,
    )

    winner = choose_style(
        [question, other],
        {f"q{question.pk}": str(choice_left.pk), f"q{other.pk}": str(choice_right.pk)},
    )

    assert winner is not None
    assert winner.slug == "lewy"


@pytest.mark.django_db
def test_extra_style_must_differ():
    style = Style.objects.get(slug="boks")
    question = Question.objects.create(text_pl="Pytanie", text_en="Question", sort_order=80)
    choice = Choice(
        question=question,
        text_pl="To samo",
        text_en="Same",
        style=style,
        points=1,
        extra_style=style,
        extra_points=1,
        sort_order=1,
    )

    with pytest.raises(ValidationError):
        choice.full_clean()
