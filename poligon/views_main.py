from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from django.db.models import F, Max, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from .heuristics import assess_language_sample, coaching_hint
from .identity import learner_state
from .models import ChoiceOption, Exercise, LearnerState, Review, StudyEvent, Submission, VocabularyItem
from .services import due_review_count, schedule_review, skill_scores

LEVELS = (0, 1, 2, 3, 4, 5)
LEVEL_LABELS = {
    0: ("No practical use", "Brak praktyki"),
    1: ("Survival", "Przetrwanie"),
    2: ("Functional", "Funkcjonalny"),
    3: ("Professional", "Zawodowy"),
    4: ("Advanced", "Zaawansowany"),
    5: ("Highly articulate", "Bardzo biegły"),
}
SKILL_LABELS = {
    "L": ("Listening", "Słuchanie"),
    "S": ("Speaking", "Mówienie"),
    "R": ("Reading", "Czytanie"),
    "W": ("Writing", "Pisanie"),
}
CHOICE_TYPES = frozenset({"mcq", "listening"})


def home(request: HttpRequest) -> HttpResponse:
    return redirect("poligon:dashboard")


def dashboard(request: HttpRequest) -> HttpResponse:
    state = learner_state(request)
    subs = list(Submission.objects.filter(learner=state).select_related("exercise")[:200])
    today_minutes = sum(
        event.minutes
        for event in StudyEvent.objects.filter(
            learner=state,
            created_at__date=timezone.localdate(),
        )
    )
    studied = StudyEvent.objects.filter(
        learner=state,
        created_at__gte=timezone.now() - timedelta(days=7),
    ).count()
    goal = max(1, state.daily_minutes)
    return render(
        request,
        "poligon/dashboard.html",
        {
            "state": state,
            "scores": skill_scores(subs),
            "due_reviews": due_review_count(state),
            "recent": subs[:6],
            "exercise_count": Exercise.objects.filter(active=True, level=state.practice_level).count(),
            "level_en": LEVEL_LABELS[state.practice_level][0],
            "level_pl": LEVEL_LABELS[state.practice_level][1],
            "studied": studied,
            "today_minutes": today_minutes,
            "today_progress": min(100, round(today_minutes / goal * 100)),
            "minutes_left": max(0, state.daily_minutes - today_minutes),
            # Only nag once there is work worth losing.
            "show_guest_banner": not request.user.is_authenticated and bool(subs),
            "show_onboarding": not subs,
        },
    )


def practice(request: HttpRequest) -> HttpResponse:
    state = learner_state(request)
    skill = request.GET.get("skill", "")
    exercise = _next_exercise(state, skill, state.practice_level)
    if not exercise:
        labels = SKILL_LABELS.get(skill)
        return render(
            request,
            "poligon/empty.html",
            {
                "level": state.practice_level,
                "skill_label_en": labels[0] if labels else "",
                "skill_label_pl": labels[1] if labels else "",
            },
        )
    return redirect("poligon:exercise", slug=exercise.slug)


def _next_exercise(state: LearnerState, skill: str, level: int) -> Exercise | None:
    """Never-tried items first, then the one this learner finished longest ago."""
    exercises = Exercise.objects.filter(active=True, level=level)
    if skill in SKILL_LABELS:
        exercises = exercises.filter(skill=skill)
    return (
        exercises.annotate(
            last_done=Max(
                "submission__completed_at",
                filter=Q(submission__learner=state),
            )
        )
        .order_by(F("last_done").asc(nulls_first=True), "id")
        .first()
    )


@ratelimit(key="ip", rate="20/m", method="POST", block=True)
def exercise(request: HttpRequest, slug: str) -> HttpResponse:
    state = learner_state(request)
    item = get_object_or_404(Exercise.objects.prefetch_related("options"), slug=slug, active=True)
    if request.method == "POST":
        submission = _record_submission(state, item, request)
        return redirect("poligon:result", submission_id=submission.pk)
    return render(
        request,
        "poligon/exercise.html",
        {"exercise": item, "script": item.content_en or item.prompt_en},
    )


def _record_submission(state: LearnerState, item: Exercise, request: HttpRequest) -> Submission:
    answer = request.POST.get("answer", "").strip()
    option_id = request.POST.get("option_id")
    selected = None
    if option_id:
        selected = get_object_or_404(ChoiceOption, pk=option_id, exercise=item)
    if item.exercise_type in CHOICE_TYPES:
        correct = bool(selected and selected.is_correct)
        score = 100.0 if correct else 0.0
        feedback: dict = {"correct": correct, "choice_result": True}
    else:
        feedback = assess_language_sample(answer)
        score = float(feedback["overall"])
    submission = Submission.objects.create(
        learner=state,
        exercise=item,
        answer_text=answer,
        selected_option=selected,
        score=score,
        feedback=feedback,
    )
    StudyEvent.objects.create(
        learner=state,
        skill=item.skill,
        minutes=item.expected_minutes,
        note=item.title_en[:200],
    )
    return submission


def result(request: HttpRequest, submission_id: int) -> HttpResponse:
    """Own page for the answer, so a reload never submits twice."""
    state = learner_state(request)
    submission = get_object_or_404(
        Submission.objects.select_related("exercise", "selected_option"),
        pk=submission_id,
        learner=state,
    )
    item = submission.exercise
    correct_option = None
    hint_en = hint_pl = ""
    if item.exercise_type in CHOICE_TYPES:
        correct_option = item.options.filter(is_correct=True).first()
    else:
        hint_en, hint_pl = coaching_hint(submission.feedback or {})
    return render(
        request,
        "poligon/result.html",
        {
            "submission": submission,
            "exercise": item,
            "feedback": submission.feedback,
            "selected_option": submission.selected_option,
            "correct_option": correct_option,
            "explanation": item.explanation_pl,
            "hint_en": hint_en,
            "hint_pl": hint_pl,
        },
    )


def reviews(request: HttpRequest) -> HttpResponse:
    state = learner_state(request)
    review = _due_review(state, state.practice_level)
    if not review:
        for item in VocabularyItem.objects.filter(active=True, level=state.practice_level)[:12]:
            Review.objects.get_or_create(
                learner=state,
                item=item,
                defaults={"due_at": timezone.now()},
            )
        review = _due_review(state, state.practice_level)
    return render(request, "poligon/reviews.html", {"review": review})


def _due_review(state: LearnerState, level: int) -> Review | None:
    return (
        Review.objects.filter(
            learner=state,
            due_at__lte=timezone.now(),
            item__level=level,
        )
        .select_related("item")
        .first()
    )


@require_POST
@ratelimit(key="ip", rate="30/m", method="POST", block=True)
def grade_review(request: HttpRequest, review_id: int) -> HttpResponse:
    state = learner_state(request)
    review = get_object_or_404(Review, id=review_id, learner=state)
    grade_raw = request.POST.get("grade", "")
    if grade_raw.isdigit():
        schedule_review(review, int(grade_raw))
        StudyEvent.objects.create(
            learner=state,
            skill="R",
            minutes=2,
            note="Vocabulary review",
        )
    return redirect("poligon:reviews")


@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def settings_view(request: HttpRequest) -> HttpResponse:
    state = learner_state(request)
    form_error = False
    if request.method == "POST":
        form_error = not _apply_settings(state, request)
        if not form_error:
            return redirect("poligon:dashboard")
    return render(
        request,
        "poligon/settings.html",
        {
            "state": state,
            "form_error": form_error,
            "level_choices": [
                {
                    "value": level,
                    "en": f"{level} — {LEVEL_LABELS[level][0]}",
                    "pl": f"{level} — {LEVEL_LABELS[level][1]}",
                }
                for level in LEVELS
            ],
        },
    )


def _apply_settings(state: LearnerState, request: HttpRequest) -> bool:
    level_raw = request.POST.get("practice_level", "").strip()
    if level_raw not in {str(level) for level in LEVELS}:
        return False
    level = int(level_raw)
    minutes_raw = request.POST.get("daily_minutes", "").strip()
    if not minutes_raw.isdigit():
        return False
    minutes = int(minutes_raw)
    if minutes < 10 or minutes > 180:
        return False
    date_raw = request.POST.get("target_date", "").strip()
    target_date = None
    if date_raw:
        try:
            target_date = date.fromisoformat(date_raw)
        except ValueError:
            return False
    state.practice_level = level
    state.target_profile = str(level) * 4
    state.daily_minutes = minutes
    state.target_date = target_date
    state.save(
        update_fields=["practice_level", "target_profile", "daily_minutes", "target_date", "updated_at"]
    )
    return True


PLACEMENT_LEVELS = (1, 2, 3, 4, 5)
PLACEMENT_PER_LEVEL = 2


@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def placement(request: HttpRequest) -> HttpResponse:
    """A short reading check, so nobody has to guess their own level."""
    state = learner_state(request)
    questions = _placement_questions()
    if not questions:
        return render(request, "poligon/empty.html", {"level": state.practice_level})
    if request.method == "POST":
        correct = sum(1 for question in questions if _is_answer_correct(question, request.POST))
        # Questions run easy to hard, so two right answers are worth one level.
        suggested = min(max(PLACEMENT_LEVELS), correct // 2)
        return render(
            request,
            "poligon/placement_result.html",
            {
                "state": state,
                "correct": correct,
                "total": len(questions),
                "suggested": suggested,
                "level_en": LEVEL_LABELS[suggested][0],
                "level_pl": LEVEL_LABELS[suggested][1],
            },
        )
    return render(request, "poligon/placement.html", {"questions": questions})


def _placement_questions() -> list[Exercise]:
    questions: list[Exercise] = []
    for level in PLACEMENT_LEVELS:
        questions += list(
            Exercise.objects.filter(active=True, exercise_type="mcq", level=level)
            .prefetch_related("options")
            .order_by("id")[:PLACEMENT_PER_LEVEL]
        )
    return questions


def _is_answer_correct(question: Exercise, posted) -> bool:
    picked = posted.get(f"q{question.pk}", "")
    return any(option.is_correct and str(option.pk) == picked for option in question.options.all())


def sources(request: HttpRequest) -> HttpResponse:
    learner_state(request)
    registry_path = Path(__file__).resolve().parent / "data" / "sources_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    return render(request, "poligon/sources.html", {"sources": registry})
