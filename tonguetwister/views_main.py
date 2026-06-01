import asyncio
import hashlib
import logging

import sentry_sdk
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .chatbot import Chatbot
from .forms import AvatarUploadForm
from .models import (
    Articulator,
    Exercise,
    Funfact,
    OldPolish,
    Trivia,
    Twister,
    UserProfileArticulator,
    UserProfileExercise,
    UserProfileTwister,
)
from .view_helpers import (
    build_exercises_pdf_response,
    build_user_content_context,
)
from .view_helpers import (
    load_more_generic as _load_more_generic,
)
from .view_helpers import (
    load_more_old_polish as _load_more_old_polish,
)
from .view_helpers import (
    simple_load_more_generic as _simple_load_more_generic,
)

logger = logging.getLogger(__name__)


def is_admin(user):
    return user.is_staff or user.is_superuser


def main(request):
    try:
        context = {
            "twisters": Twister.objects.all()[:1],
            "articulators": Articulator.objects.all()[:1],
            "exercises": Exercise.objects.all()[:1],
            "trivia": Trivia.objects.all()[:0],
            "funfacts": Funfact.objects.all()[:0],
            "old_polish_texts": OldPolish.objects.order_by("?").first(),
        }

        if request.user.is_authenticated:
            context.update(
                {
                    "user_twisters_texts": list(
                        UserProfileTwister.objects.filter(user=request.user)
                        .select_related("twister")
                        .values_list("twister__text", flat=True)
                    ),
                    "user_articulators_texts": list(
                        UserProfileArticulator.objects.filter(user=request.user)
                        .select_related("articulator")
                        .values_list("articulator__text", flat=True)
                    ),
                    "user_exercises_texts": list(
                        UserProfileExercise.objects.filter(user=request.user)
                        .select_related("exercise")
                        .values_list("exercise__text", flat=True)
                    ),
                }
            )

        return render(request, "tonguetwister/main.html", context)
    except Exception:
        logger.exception("Exception occurred in main view")
        return HttpResponse("Internal Server Error", status=500)


_chatbot_instance = None


def get_chatbot():
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = Chatbot()
    return _chatbot_instance


async def chatbot(request):
    try:
        if not settings.FEATURE_CHATBOT_ENABLED:
            return JsonResponse({"detail": "Not found."}, status=404)

        user_input = request.GET.get("message", "").strip()
        if not user_input:
            return JsonResponse({"response": "Nie rozumiem."})

        if len(user_input) > settings.CHATBOT_MAX_INPUT_LENGTH:
            return JsonResponse({"response": "Wiadomość jest za długa."}, status=400)

        cache_key = f"chatbot:view:response:{hashlib.sha256(user_input.encode('utf-8')).hexdigest()}"
        cached_response = cache.get(cache_key)
        if cached_response:
            return JsonResponse({"response": cached_response})

        try:
            response = await asyncio.wait_for(
                sync_to_async(get_chatbot().get_response)(user_input),
                timeout=settings.CHATBOT_RESPONSE_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError:
            return JsonResponse({"response": "Przekroczono czas przetwarzania."}, status=503)

        cache.set(cache_key, response, timeout=3600)
        return JsonResponse({"response": response})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return JsonResponse({"response": "Wystąpił błąd. Spróbuj ponownie później."})


@user_passes_test(is_admin)
def content_management(request):
    return render(request, "tonguetwister/admin/settings.html")


def error_404_view(request, exception):
    return render(request, "tonguetwister/404.html", {})


def load_more_generic(request, model, user_profile_model, related_field, limit=1):
    return _load_more_generic(request, model, user_profile_model, related_field, limit=limit, logger=logger)


def load_more_articulators(request):
    return load_more_generic(request, Articulator, UserProfileArticulator, related_field="articulator")


def load_more_exercises(request):
    return load_more_generic(request, Exercise, UserProfileExercise, related_field="exercise")


def load_more_twisters(request):
    return load_more_generic(request, Twister, UserProfileTwister, related_field="twister")


def simple_load_more_generic(request, model, limit=1):
    return _simple_load_more_generic(request, model, limit=limit, logger=logger)


def load_more_trivia(request):
    return simple_load_more_generic(request, Trivia)


def load_more_funfacts(request):
    return simple_load_more_generic(request, Funfact)


def load_more_old_polish(request):
    return _load_more_old_polish(request, logger=logger)


@login_required
def user_content(request):
    profile = request.user.profile

    if request.method == "POST":
        if "action" in request.POST and request.POST["action"] == "delete-avatar":
            if profile.avatar:
                profile.avatar.delete(save=True)
            else:
                return redirect("user_content")

        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("user_content")
    else:
        form = AvatarUploadForm(instance=request.user.profile)

    context = build_user_content_context(request.user, form)

    if "export" in request.GET and request.GET["export"] == "exercises":
        return build_exercises_pdf_response(context, settings.BASE_DIR)

    return render(request, "tonguetwister/users/user-content.html", context)


@login_required
@csrf_protect
@require_http_methods(["POST"])
def add_articulator(request, articulator_id):
    user = request.user
    articulator = get_object_or_404(Articulator, id=articulator_id)
    if UserProfileArticulator.objects.filter(user=user, articulator=articulator).exists():
        return JsonResponse({"status": "Duplicate articulator"})
    user_articulator = UserProfileArticulator.objects.create(user=user, articulator=articulator)
    return JsonResponse({"status": "Articulator added", "userArticulatorId": user_articulator.id})


@login_required
@csrf_protect
@require_http_methods(["POST"])
def delete_articulator(request, articulator_id):
    user = request.user
    articulator = get_object_or_404(UserProfileArticulator, id=articulator_id, user=user)
    articulator.delete()
    return JsonResponse({"status": "Articulator deleted"})


@login_required
@csrf_protect
@require_http_methods(["POST"])
def add_exercise(request, exercise_id):
    user = request.user
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if UserProfileExercise.objects.filter(user=user, exercise=exercise).exists():
        return JsonResponse({"status": "Duplicate exercise"})
    user_exercise = UserProfileExercise.objects.create(user=user, exercise=exercise)
    return JsonResponse({"status": "Exercise added", "userExerciseId": user_exercise.id})


@login_required
@csrf_protect
@require_http_methods(["POST"])
def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(UserProfileExercise, id=exercise_id, user=request.user)
    exercise.delete()
    return JsonResponse({"status": "Exercise deleted"})


@login_required
@csrf_protect
@require_http_methods(["POST"])
def add_twister(request, twister_id):
    user = request.user
    twister = get_object_or_404(Twister, id=twister_id)
    if UserProfileTwister.objects.filter(user=user, twister=twister).exists():
        return JsonResponse({"status": "Duplicate twister"})
    user_twister = UserProfileTwister.objects.create(user=user, twister=twister)
    return JsonResponse({"status": "Twister added", "userTwisterId": user_twister.id})


@login_required
@csrf_protect
@require_http_methods(["POST"])
def delete_twister(request, twister_id):
    twister = get_object_or_404(UserProfileTwister, id=twister_id, user=request.user)
    twister.delete()
    return JsonResponse({"status": "Twister deleted"})


