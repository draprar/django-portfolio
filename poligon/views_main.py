from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from .heuristics import assess_language_sample, coaching_hint
from .identity import (
    ACCOUNT_HINT_KEY,
    ATTEMPT_KEY,
    account_state,
    current_plan,
    guest_level,
    remember_seen,
    seen_slugs,
    set_guest_level,
    shuffle_seed,
)
from .models import ChoiceOption, Exercise, LearnerState, Review, StudyEvent, Submission, VocabularyItem
from .reference import REFERENCE_TABLES
from .services import due_review_count, schedule_review, skill_scores

LEVELS = (0, 1, 2, 3, 4, 5)
LEVEL_LABELS = {
    0: ("No practical use", "Brak praktyki"),
    1: ("Survival", "Przetrwanie"),
    2: ("Functional", "Funkcjonalny"),
    3: ("Operational", "Operacyjny"),
    4: ("Advanced", "Zaawansowany"),
    5: ("Fully proficient", "Pełna sprawność"),
}
LEVEL_HINTS = {
    0: ("Single words.", "Pojedyncze słowa."),
    1: ("One order, one fact.", "Jeden rozkaz, jeden fakt."),
    2: ("Everyday duty: rations, time, route.", "Codzienna służba: racje, godzina, trasa."),
    3: ("Orders, details, radio traffic.", "Rozkazy, szczegóły, łączność."),
    4: ("Briefing with reasons.", "Odprawa z uzasadnieniem."),
    5: ("Full report with a fallback plan.", "Pełny meldunek z planem zastępczym."),
}
SKILL_LABELS = {
    "L": ("Listening", "Słuchanie"),
    "S": ("Speaking", "Mówienie"),
    "R": ("Reading", "Czytanie"),
    "W": ("Writing", "Pisanie"),
}
CHOICE_TYPES = frozenset({"mcq", "listening"})


@dataclass(frozen=True)
class Attempt:
    """One checked answer, whether or not it was stored."""

    score: float
    answer_text: str


def home(request: HttpRequest) -> HttpResponse:
    return redirect("poligon:dashboard")


def start(request: HttpRequest) -> HttpResponse:
    """Where a visit begins: what this is, then one choice of level."""
    if request.user.is_authenticated:
        return redirect("poligon:dashboard")
    form_error = False
    if request.method == "POST":
        raw = request.POST.get("practice_level", "").strip()
        if raw in {str(level) for level in LEVELS}:
            set_guest_level(request, int(raw))
            return redirect("poligon:dashboard")
        form_error = True
    return render(
        request,
        "poligon/start.html",
        {
            "levels": _level_choices(),
            "current_level": guest_level(request),
            "form_error": form_error,
        },
    )


def _level_choices() -> list[dict]:
    return [
        {
            "value": level,
            "name_en": LEVEL_LABELS[level][0],
            "name_pl": LEVEL_LABELS[level][1],
            "hint_en": LEVEL_HINTS[level][0],
            "hint_pl": LEVEL_HINTS[level][1],
        }
        for level in LEVELS
    ]


def dashboard(request: HttpRequest) -> HttpResponse:
    plan = current_plan(request)
    if plan is None:
        return redirect("poligon:start")
    state = account_state(request)
    subs = list(Submission.objects.filter(learner=state).select_related("exercise")[:200]) if state else []
    today_minutes = 0
    studied = 0
    if state is not None:
        today_minutes = sum(
            event.minutes
            for event in StudyEvent.objects.filter(learner=state, created_at__date=timezone.localdate())
        )
        studied = StudyEvent.objects.filter(
            learner=state,
            created_at__gte=timezone.now() - timedelta(days=7),
        ).count()
    goal = max(1, plan.daily_minutes)
    return render(
        request,
        "poligon/dashboard.html",
        {
            "state": plan,
            "scores": skill_scores(subs),
            "due_reviews": due_review_count(state) if state else 0,
            "recent": subs[:6],
            "left": _remaining(request, state, "", plan.practice_level).count(),
            "level_en": LEVEL_LABELS[plan.practice_level][0],
            "level_pl": LEVEL_LABELS[plan.practice_level][1],
            "studied": studied,
            "today_minutes": today_minutes,
            "today_progress": min(100, round(today_minutes / goal * 100)),
            "minutes_left": max(0, plan.daily_minutes - today_minutes),
            "show_onboarding": state is not None and not subs,
        },
    )


def practice(request: HttpRequest) -> HttpResponse:
    plan = current_plan(request)
    if plan is None:
        return redirect("poligon:start")
    skill = request.GET.get("skill", "")
    state = account_state(request)
    item = _remaining(request, state, skill, plan.practice_level).order_by("id").first()
    if item is not None:
        return redirect("poligon:exercise", slug=item.slug)
    labels = SKILL_LABELS.get(skill)
    return render(
        request,
        "poligon/empty.html",
        {
            "level": plan.practice_level,
            "skill_label_en": labels[0] if labels else "",
            "skill_label_pl": labels[1] if labels else "",
            # Nothing left is a finished pool; nothing at all is an empty one.
            "finished": _pool(skill, plan.practice_level).exists(),
        },
    )


def _pool(skill: str, level: int) -> QuerySet[Exercise]:
    exercises = Exercise.objects.filter(active=True, level=level)
    return exercises.filter(skill=skill) if skill in SKILL_LABELS else exercises


def _remaining(
    request: HttpRequest,
    state: LearnerState | None,
    skill: str,
    level: int,
) -> QuerySet[Exercise]:
    """What this learner has not answered yet. Nothing is ever served twice."""
    exercises = _pool(skill, level)
    if state is not None:
        return exercises.exclude(pk__in=Submission.objects.filter(learner=state).values("exercise_id"))
    return exercises.exclude(slug__in=seen_slugs(request))


@ratelimit(key="ip", rate="20/m", method="POST", block=True)
def exercise(request: HttpRequest, slug: str) -> HttpResponse:
    plan = current_plan(request)
    if plan is None:
        return redirect("poligon:start")
    item = get_object_or_404(Exercise.objects.prefetch_related("options"), slug=slug, active=True)
    if request.method == "POST":
        state = account_state(request)
        if state is not None:
            submission = _record_submission(state, item, request)
            return redirect("poligon:result", submission_id=submission.pk)
        _remember_attempt(request, item)
        return redirect("poligon:last_result")
    return render(
        request,
        "poligon/exercise.html",
        {
            "exercise": item,
            "options": _shuffled_options(item, shuffle_seed(request)),
            "script": item.content_en or item.prompt_en,
        },
    )


def _account_or_404(request: HttpRequest) -> LearnerState:
    """For pages behind ``login_required``, where a guest never arrives."""
    state = account_state(request)
    if state is None:
        raise Http404
    return state


def _shuffled_options(item: Exercise, seed: str) -> list[ChoiceOption]:
    """The right answer must not always sit first. Same seed, same order."""
    options = list(item.options.all())
    random.Random(f"{seed}:{item.pk}").shuffle(options)  # noqa: S311 — display order, not a secret
    return options


def _selected_option(request: HttpRequest, item: Exercise) -> ChoiceOption | None:
    option_id = request.POST.get("option_id")
    if not option_id:
        return None
    return get_object_or_404(ChoiceOption, pk=option_id, exercise=item)


def _grade(item: Exercise, answer: str, selected: ChoiceOption | None) -> tuple[float, dict]:
    if item.exercise_type in CHOICE_TYPES:
        correct = bool(selected and selected.is_correct)
        return (100.0 if correct else 0.0), {"correct": correct, "choice_result": True}
    feedback = assess_language_sample(answer)
    return float(feedback["overall"]), feedback


def _record_submission(state: LearnerState, item: Exercise, request: HttpRequest) -> Submission:
    answer = request.POST.get("answer", "").strip()
    selected = _selected_option(request, item)
    score, feedback = _grade(item, answer, selected)
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


def _remember_attempt(request: HttpRequest, item: Exercise) -> None:
    """A guest's answer lives in the session, so the database stays untouched."""
    answer = request.POST.get("answer", "").strip()
    selected = _selected_option(request, item)
    score, feedback = _grade(item, answer, selected)
    request.session[ATTEMPT_KEY] = {
        "exercise_id": item.pk,
        "score": score,
        "answer": answer,
        "feedback": feedback,
        "selected_option_id": selected.pk if selected else None,
    }
    remember_seen(request, item.slug)


def result(request: HttpRequest, submission_id: int) -> HttpResponse:
    """Own page for the answer, so a reload never submits twice."""
    state = account_state(request)
    if state is None:
        raise Http404
    submission = get_object_or_404(
        Submission.objects.select_related("exercise", "selected_option"),
        pk=submission_id,
        learner=state,
    )
    return _render_result(
        request,
        submission.exercise,
        Attempt(submission.score or 0.0, submission.answer_text),
        submission.feedback or {},
        submission.selected_option,
        show_account_hint=False,
    )


def last_result(request: HttpRequest) -> HttpResponse:
    """The answer a guest has just checked. Read from the session, never stored."""
    attempt = request.session.get(ATTEMPT_KEY)
    if request.user.is_authenticated or not isinstance(attempt, dict):
        return redirect("poligon:dashboard")
    item = get_object_or_404(Exercise, pk=attempt.get("exercise_id"), active=True)
    selected = None
    if attempt.get("selected_option_id"):
        selected = ChoiceOption.objects.filter(pk=attempt["selected_option_id"], exercise=item).first()
    # Say it once per visit, right after there is something worth keeping.
    show_account_hint = not request.session.get(ACCOUNT_HINT_KEY)
    if show_account_hint:
        request.session[ACCOUNT_HINT_KEY] = True
    return _render_result(
        request,
        item,
        Attempt(float(attempt.get("score") or 0.0), str(attempt.get("answer") or "")),
        attempt.get("feedback") or {},
        selected,
        show_account_hint=show_account_hint,
    )


def _render_result(
    request: HttpRequest,
    item: Exercise,
    attempt: Attempt,
    feedback: dict,
    selected_option: ChoiceOption | None,
    *,
    show_account_hint: bool,
) -> HttpResponse:
    correct_option = None
    hint_en = hint_pl = ""
    if item.exercise_type in CHOICE_TYPES:
        correct_option = item.options.filter(is_correct=True).first()
    else:
        hint_en, hint_pl = coaching_hint(feedback)
    return render(
        request,
        "poligon/result.html",
        {
            "submission": attempt,
            "exercise": item,
            "feedback": feedback,
            "selected_option": selected_option,
            "correct_option": correct_option,
            "explanation": item.explanation_pl,
            "hint_en": hint_en,
            "hint_pl": hint_pl,
            "show_account_hint": show_account_hint,
        },
    )


def reviews(request: HttpRequest) -> HttpResponse:
    state = account_state(request)
    if state is None:
        return render(request, "poligon/reviews.html", {"needs_account": True})
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
    state = account_state(request)
    if state is None:
        return redirect("poligon:reviews")
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


@login_required(login_url="poligon:login")
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def settings_view(request: HttpRequest) -> HttpResponse:
    state = _account_or_404(request)
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


@login_required(login_url="poligon:login")
@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def placement(request: HttpRequest) -> HttpResponse:
    """A short reading check, so nobody has to guess their own level."""
    state = _account_or_404(request)
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
    seed = shuffle_seed(request)
    return render(
        request,
        "poligon/placement.html",
        {
            "questions": [
                {"item": question, "options": _shuffled_options(question, seed)} for question in questions
            ],
            "total": len(questions),
        },
    )


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


def tables(request: HttpRequest) -> HttpResponse:
    """Reference sheets. Nothing here is graded or stored."""
    return render(request, "poligon/tables.html", {"tables": REFERENCE_TABLES})


def policy(request: HttpRequest) -> HttpResponse:
    return render(request, "poligon/policy.html")
