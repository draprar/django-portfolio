from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from .events import record_event
from .framework import PLACEMENT_VERSION, WRITING_EVAL_V2, suggest_placement_level
from .heuristics import coaching_hint
from .i18n import LANG_KEY, SUPPORTED
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
from .learning import assess_writing_v2, one_improvement
from .levels import LEVEL_HINTS, LEVEL_LABELS, LEVELS, level_names
from .models import (
    ChoiceOption,
    Exercise,
    LearnerState,
    PlacementAttempt,
    Review,
    StudyEvent,
    Submission,
)
from .reference import REFERENCE_TABLES
from .services import (
    NEW_CARDS_PER_SESSION,
    VOCABULARY_SKILL,
    due_review_count,
    next_vocabulary_card,
    schedule_review,
    skill_scores,
)

SKILL_LABELS = {
    "L": ("Listening", "Słuchanie"),
    "S": ("Speaking", "Mówienie"),
    "R": ("Reading", "Czytanie"),
    "W": ("Writing", "Pisanie"),
}
SKILL_PLAN = {
    "L": ("Listen to one message", "Posłuchaj jednego komunikatu"),
    "S": ("Say a short answer", "Powiedz krótką odpowiedź"),
    "R": ("Read one note", "Przeczytaj jedną notatkę"),
    "W": ("Write a short note", "Napisz krótką notatkę"),
}
SKILL_OF = {
    "L": "ze słuchania",
    "S": "z mówienia",
    "R": "z czytania",
    "W": "z pisania",
}


def polish_count(count: int, one: str, few: str, many: str) -> str:
    """Polish numeral agreement: 1 sesja, 2 sesje, 5 sesji, 12 sesji, 22 sesje."""
    n = abs(int(count))
    if n == 1:
        word = one
    elif n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        word = few
    else:
        word = many
    return f"{count} {word}"


CHOICE_TYPES = frozenset({"mcq", "listening", "true_false"})
VOCAB_INTRO_KEY = "poligon_vocab_new"
OPEN_KEY = "poligon_open_slug"


@dataclass(frozen=True)
class Attempt:
    """One checked answer, whether or not it was stored."""

    score: float
    answer_text: str


def home(request: HttpRequest) -> HttpResponse:
    return redirect("poligon:dashboard")


@require_POST
def set_language(request: HttpRequest) -> HttpResponse:
    """Remember PL or EN for the interface. Exercise text is not translated here."""
    lang = request.POST.get("lang", "")
    current = request.session.get(LANG_KEY, "pl")
    if lang in SUPPORTED:
        if lang != current:
            record_event(request, "language_changed", {"lang": lang})
        request.session[LANG_KEY] = lang
    target = request.POST.get("next", "")
    if not target.startswith("/cwiczba/"):
        target = reverse("poligon:dashboard")
    return redirect(target)


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
    scores = skill_scores(subs)
    remaining = {
        skill: _remaining(request, state, skill, plan.practice_level).order_by("id").first()
        for skill in SKILL_LABELS
    }
    focus = _focus_skill(scores, remaining)
    return render(
        request,
        "poligon/dashboard.html",
        {
            "state": plan,
            "scores": scores,
            "due_reviews": due_review_count(state) if state else 0,
            "recent": subs[:6],
            "left": _remaining(request, state, "", plan.practice_level).count(),
            "level_en": level_names(plan.practice_level)[0],
            "level_pl": level_names(plan.practice_level)[1],
            "studied": studied,
            "studied_pl": polish_count(studied, "sesja", "sesje", "sesji"),
            "today_minutes": today_minutes,
            "today_progress": min(100, round(today_minutes / goal * 100)),
            "minutes_left": max(0, plan.daily_minutes - today_minutes),
            "show_onboarding": state is not None and not subs,
            "focus": focus,
            "focus_en": SKILL_LABELS[focus][0] if focus else "",
            "focus_pl": SKILL_LABELS[focus][1] if focus else "",
            "now": remaining.get(focus) if focus else None,
            "daily_plan": _daily_tasks(remaining, focus, plan.daily_minutes, state is not None),
        },
    )


def _focus_skill(scores: dict[str, int], remaining: dict[str, Exercise | None]) -> str | None:
    """The skill to work on: the weakest one that still has an exercise."""
    candidates = [skill for skill, item in remaining.items() if item is not None]
    if not candidates:
        return None
    return min(candidates, key=lambda skill: (scores.get(skill, 0), skill))


def _daily_tasks(remaining: dict[str, Exercise | None], focus: str | None, minutes: int, has_account: bool) -> list[dict]:
    """Two or three tasks for the day, taken from the plan the learner already set."""
    tasks: list[dict] = []
    item = remaining.get(focus) if focus else None
    if item is not None and focus:
        tasks.append(
            {
                "kind": "exercise",
                "slug": item.slug,
                "en": SKILL_PLAN[focus][0],
                "pl": SKILL_PLAN[focus][1],
            }
        )
    if has_account:
        tasks.append({"kind": "flashcards", "slug": "", "en": "Review the flashcards", "pl": "Powtórz fiszki"})
    if minutes >= 21:
        for skill, item in remaining.items():
            if item is None or skill == focus:
                continue
            tasks.append(
                {
                    "kind": "exercise",
                    "slug": item.slug,
                    "en": SKILL_PLAN[skill][0],
                    "pl": SKILL_PLAN[skill][1],
                }
            )
            break
    return tasks[:3]


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
            "skill_of": SKILL_OF.get(skill, ""),
            # Nothing left is a finished pool; nothing at all is an empty one.
            "finished": _pool(skill, plan.practice_level).exists(),
        },
    )


def _pool(skill: str, level: int) -> QuerySet[Exercise]:
    exercises = Exercise.objects.filter(active=True, level=level, catalog_role="practice")
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
    if item.level != plan.practice_level:
        raise Http404
    if request.method == "POST":
        if item.exercise_type in CHOICE_TYPES and not request.POST.get("option_id"):
            return _render_exercise(request, item, choice_error=True)
        if item.exercise_type not in CHOICE_TYPES and not request.POST.get("answer", "").strip():
            return _render_exercise(request, item, answer_error=True)
        state = account_state(request)
        _note_exercise_done(request, item)
        if state is not None:
            submission = _record_submission(state, item, request)
            return redirect("poligon:result", submission_id=submission.pk)
        _remember_attempt(request, item)
        return redirect("poligon:last_result")
    _note_exercise_open(request, item)
    return _render_exercise(request, item)


def _render_exercise(
    request: HttpRequest,
    item: Exercise,
    *,
    choice_error: bool = False,
    answer_error: bool = False,
) -> HttpResponse:
    delivery = item.delivery if isinstance(item.delivery, dict) else {}
    return render(
        request,
        "poligon/exercise.html",
        {
            "exercise": item,
            "options": _shuffled_options(item, shuffle_seed(request)),
            "script": delivery.get("transcript") or item.content_en or item.prompt_en,
            "delivery": delivery,
            "level_en": level_names(item.level)[0],
            "level_pl": level_names(item.level)[1],
            "choice_error": choice_error,
            "answer_error": answer_error,
        },
    )


def _note_exercise_open(request: HttpRequest, item: Exercise) -> None:
    previous = request.session.get(OPEN_KEY)
    if isinstance(previous, str) and previous != item.slug:
        record_event(request, "exercise_abandoned", {"slug": previous})
    request.session[OPEN_KEY] = item.slug
    record_event(request, "exercise_started", {"slug": item.slug, "skill": item.skill, "level": item.level})


def _note_exercise_done(request: HttpRequest, item: Exercise) -> None:
    request.session.pop(OPEN_KEY, None)
    record_event(request, "exercise_completed", {"slug": item.slug, "skill": item.skill})


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
    criteria = item.success_criteria if isinstance(item.success_criteria, list) else []
    feedback = assess_writing_v2(answer, criteria)
    return float(feedback["overall"]), feedback


def _record_submission(state: LearnerState, item: Exercise, request: HttpRequest) -> Submission:
    """Store one new attempt. A second POST is another attempt, not a refresh."""
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
        "level": item.level,
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
    if submission.exercise.level != state.practice_level:
        return redirect("poligon:dashboard")
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
    plan = current_plan(request)
    if request.user.is_authenticated or not isinstance(attempt, dict) or plan is None:
        return redirect("poligon:dashboard")
    item = get_object_or_404(Exercise, pk=attempt.get("exercise_id"), active=True)
    if item.level != plan.practice_level or attempt.get("level") not in (None, plan.practice_level):
        request.session.pop(ATTEMPT_KEY, None)
        return redirect("poligon:dashboard")
    selected = None
    if attempt.get("selected_option_id"):
        selected = ChoiceOption.objects.filter(pk=attempt["selected_option_id"], exercise=item).first()
    # Say it once per visit, right after there is something worth keeping.
    show_account_hint = len(seen_slugs(request)) >= 3 and not request.session.get(ACCOUNT_HINT_KEY)
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
    elif feedback.get("evaluator_version") == WRITING_EVAL_V2:
        hint_en, hint_pl = one_improvement(feedback, item.level)
    else:
        hint_en, hint_pl = coaching_hint(feedback, item.level)
    names = level_names(item.level)
    step = _next_step(request, item)
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
            "level_en": names[0],
            "level_pl": names[1],
            **step,
        },
    )


def _next_step(request: HttpRequest, item: Exercise) -> dict[str, str]:
    """One next action: same skill, another skill, flashcards, or a level change."""
    state = account_state(request)
    same = _remaining(request, state, item.skill, item.level).exclude(pk=item.pk).order_by("id").first()
    if same is not None:
        return {
            "next_en": "The next exercise for this same skill.",
            "next_pl": "Teraz kolejne ćwiczenie z tej samej sprawności.",
            "next_url": reverse("poligon:exercise", args=[same.slug]),
            "next_label_en": "Open it",
            "next_label_pl": "Otwórz",
        }
    for skill in SKILL_LABELS:
        if skill == item.skill:
            continue
        other = _remaining(request, state, skill, item.level).order_by("id").first()
        if other is not None:
            return {
                "next_en": f"Nothing left in this skill. Next: {SKILL_LABELS[skill][0]}.",
                "next_pl": f"Z tej sprawności nie ma już ćwiczeń. Teraz {SKILL_LABELS[skill][1].lower()}.",
                "next_url": reverse("poligon:exercise", args=[other.slug]),
                "next_label_en": "Open it",
                "next_label_pl": "Otwórz",
            }
    if state is not None and due_review_count(state):
        return {
            "next_en": "Nothing is left in this queue. Review the flashcards that are due.",
            "next_pl": "Nie ma już ćwiczeń w tej kolejce. Powtórz fiszki na dziś.",
            "next_url": reverse("poligon:reviews"),
            "next_label_en": "Flashcards",
            "next_label_pl": "Fiszki",
        }
    return {
        "next_en": "Nothing is left at this level. Change the level or open the flashcards.",
        "next_pl": "Na tym poziomie nie ma już ćwiczeń. Zmień poziom albo otwórz fiszki.",
        "next_url": reverse("poligon:start") if state is None else reverse("poligon:reviews"),
        "next_label_en": "Continue",
        "next_label_pl": "Dalej",
    }


def reviews(request: HttpRequest) -> HttpResponse:
    state = account_state(request)
    if state is None:
        return render(request, "poligon/reviews.html", {"needs_account": True})
    review, added = next_vocabulary_card(state, state.practice_level, _introductions_left(request))
    _note_introduction(request, added)
    return render(request, "poligon/reviews.html", {"review": review})


def _introductions_left(request: HttpRequest) -> int:
    raw = request.session.get(VOCAB_INTRO_KEY)
    today = timezone.localdate().isoformat()
    if not isinstance(raw, dict) or raw.get("date") != today:
        return NEW_CARDS_PER_SESSION
    try:
        used = int(raw.get("count") or 0)
    except (TypeError, ValueError):
        used = 0
    return max(0, NEW_CARDS_PER_SESSION - used)


def _note_introduction(request: HttpRequest, added: int) -> None:
    if added <= 0:
        return
    today = timezone.localdate().isoformat()
    raw = request.session.get(VOCAB_INTRO_KEY)
    used = int(raw.get("count") or 0) if isinstance(raw, dict) and raw.get("date") == today else 0
    request.session[VOCAB_INTRO_KEY] = {"date": today, "count": used + added}


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
        record_event(request, "flashcard_reviewed", {"review_id": review.pk, "grade": int(grade_raw)})
        StudyEvent.objects.create(
            learner=state,
            skill=VOCABULARY_SKILL,
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
                    "en": f"{level} — {level_names(level)[0]}",
                    "pl": f"{level} — {level_names(level)[1]}",
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


@login_required(login_url="poligon:login")
@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def placement(request: HttpRequest) -> HttpResponse:
    """A short check that suggests a starting level. It is not a qualification."""
    state = _account_or_404(request)
    questions = _placement_questions()
    if not questions:
        return render(request, "poligon/empty.html", {"level": state.practice_level})
    if request.method == "POST":
        correct = sum(1 for question in questions if _is_answer_correct(question, request.POST))
        suggested = suggest_placement_level(correct)
        PlacementAttempt.objects.create(
            learner=state,
            algorithm_version=PLACEMENT_VERSION,
            correct_count=correct,
            question_count=len(questions),
            suggested_level=suggested,
            answers=[
                {"slug": question.slug, "correct": _is_answer_correct(question, request.POST)}
                for question in questions
            ],
        )
        record_event(
            request,
            "placement_completed",
            {"suggested": suggested, "correct": correct, "algorithm": PLACEMENT_VERSION},
        )
        names = level_names(suggested)
        return render(
            request,
            "poligon/placement_result.html",
            {
                "state": state,
                "correct": correct,
                "total": len(questions),
                "suggested": suggested,
                "level_en": names[0],
                "level_pl": names[1],
            },
        )
    record_event(request, "placement_started", {"questions": len(questions)})
    seed = shuffle_seed(request)
    return render(
        request,
        "poligon/placement.html",
        {
            "questions": [
                {
                    "item": question,
                    "options": _shuffled_options(question, seed),
                    "prompt": (question.prompt_en or "").strip(),
                }
                for question in questions
            ],
            "total": len(questions),
        },
    )


def _placement_questions() -> list[Exercise]:
    """The calibrated bank. Practice exercises are not a stand-in."""
    return list(
        Exercise.objects.filter(
            catalog_role="placement",
            publication_status="published",
            exercise_type="mcq",
        )
        .prefetch_related("options")
        .order_by("level", "slug")
    )


def _is_answer_correct(question: Exercise, posted) -> bool:
    picked = posted.get(f"q{question.pk}", "")
    return any(option.is_correct and str(option.pk) == picked for option in question.options.all())


def tables(request: HttpRequest) -> HttpResponse:
    """Reference sheets. Nothing here is graded or stored."""
    return render(request, "poligon/tables.html", {"tables": REFERENCE_TABLES})


def policy(request: HttpRequest) -> HttpResponse:
    return render(request, "poligon/policy.html")
