from unittest.mock import Mock

import pytest
from django.contrib.auth.models import User

from tonguetwister.models import (
    Articulator,
    Exercise,
    Twister,
    UserProfileArticulator,
    UserProfileExercise,
    UserProfileTwister,
)
from tonguetwister.view_helpers import build_exercises_pdf_response, build_user_content_context


@pytest.mark.django_db
def test_build_user_content_context_returns_expected_lists():
    user = User.objects.create_user(username="helper-user", password="pass")
    art = Articulator.objects.create(text="arta")
    ex = Exercise.objects.create(text="exa")
    tw = Twister.objects.create(text="twa")

    UserProfileArticulator.objects.create(user=user, articulator=art)
    UserProfileExercise.objects.create(user=user, exercise=ex)
    UserProfileTwister.objects.create(user=user, twister=tw)

    form = Mock(name="avatar-form")
    context = build_user_content_context(user, form)

    assert context["form"] is form
    assert list(context["user_articulators_texts"]) == ["arta"]
    assert list(context["user_exercises_texts"]) == ["exa"]
    assert list(context["user_twisters_texts"]) == ["twa"]
    assert context["articulators"].count() == 1
    assert context["exercises"].count() == 1
    assert context["twisters"].count() == 1


@pytest.mark.django_db
def test_build_exercises_pdf_response_sets_headers_and_sanitizes_html(monkeypatch, tmp_path):
    captured_story = []

    class DummyDoc:
        def __init__(self, response, pagesize=None):
            self.response = response

        def build(self, story):
            captured_story.extend(story)
            self.response.write(b"%PDF-dummy")

    class DummyStyles(dict):
        def add(self, style):
            self[style.name] = style

    class DummyStyle:
        def __init__(self, name, **_kwargs):
            self.name = name

    monkeypatch.setattr("reportlab.pdfbase.pdfmetrics.registerFont", lambda *_args, **_kwargs: None)
    monkeypatch.setattr("reportlab.pdfbase.ttfonts.TTFont", lambda *_args, **_kwargs: object())
    monkeypatch.setattr("reportlab.platypus.SimpleDocTemplate", DummyDoc)
    monkeypatch.setattr("reportlab.lib.styles.getSampleStyleSheet", lambda: DummyStyles())
    monkeypatch.setattr("reportlab.lib.styles.ParagraphStyle", DummyStyle)
    monkeypatch.setattr("reportlab.platypus.Paragraph", lambda text, _style: ("p", text))
    monkeypatch.setattr("reportlab.platypus.Spacer", lambda w, h: ("s", w, h))

    context = {
        "user_articulators_texts": ["<b>art</b> text"],
        "user_exercises_texts": ["<script>alert(1)</script>exercise"],
        "user_twisters_texts": ["<i>twister</i>"],
    }

    response = build_exercises_pdf_response(context, str(tmp_path))

    assert response.status_code == 200
    assert response["Content-Disposition"] == 'attachment; filename="lingwolamkowe-cwiczenia.pdf"'

    paragraph_texts = [item[1] for item in captured_story if item[0] == "p"]
    assert any("Rozgrzewanie artykulatorów" in t for t in paragraph_texts)
    assert any("Ćwiczenia właściwe" in t for t in paragraph_texts)
    assert any("Łamańce językowe" in t for t in paragraph_texts)
    assert "<b>" not in " ".join(paragraph_texts)
    assert "<script>" not in " ".join(paragraph_texts)
