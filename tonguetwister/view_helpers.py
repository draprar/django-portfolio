from django.http import HttpResponse, JsonResponse

from .models import (
    Articulator,
    Exercise,
    OldPolish,
    Twister,
    UserProfileArticulator,
    UserProfileExercise,
    UserProfileTwister,
)


def load_more_generic(request, model, user_profile_model, related_field, limit=1, logger=None):
    try:
        offset = int(request.GET.get("offset", 0))
        objects = model.objects.all()[offset : offset + limit]

        if request.user.is_authenticated:
            user_texts = set(
                user_profile_model.objects.filter(user=request.user).values_list(f"{related_field}__text", flat=True)
            )
        else:
            user_texts = set()

        data = [
            {
                "id": obj.id,
                "text": getattr(obj, "text", ""),
                "is_added": obj.text in user_texts,
            }
            for obj in objects
        ]
        return JsonResponse(data, safe=False)
    except Exception:
        if logger:
            logger.exception("Exception in load_more_generic")
        return JsonResponse({"error": "Internal Server Error"}, status=500)


def simple_load_more_generic(request, model, limit=1, logger=None):
    try:
        offset = int(request.GET.get("offset", 0))
        objects = model.objects.all()[offset : offset + limit]
        data = list(objects.values())
        return JsonResponse(data, safe=False)
    except Exception:
        if logger:
            logger.exception("Exception in simple_load_more_generic")
        return JsonResponse({"error": "Internal Server Error"}, status=500)


def load_more_old_polish(request, logger=None):
    try:
        random_record = OldPolish.objects.order_by("?").values().first()
        if random_record:
            return JsonResponse([random_record], safe=False)
        return JsonResponse([], safe=False)
    except Exception:
        if logger:
            logger.exception("Exception in load_more_old_polish")
        return JsonResponse({"error": "Internal Server Error"}, status=500)


def build_user_content_context(user, form):
    user_articulators = UserProfileArticulator.objects.filter(user=user).select_related("articulator")
    user_articulators_texts = list(
        UserProfileArticulator.objects.filter(user=user).values_list("articulator__text", flat=True)
    )

    user_exercises = UserProfileExercise.objects.filter(user=user).select_related("exercise")
    user_exercises_texts = list(UserProfileExercise.objects.filter(user=user).values_list("exercise__text", flat=True))

    user_twisters = UserProfileTwister.objects.filter(user=user).select_related("twister")
    user_twisters_texts = list(UserProfileTwister.objects.filter(user=user).values_list("twister__text", flat=True))

    return {
        "form": form,
        "articulators": Articulator.objects.all(),
        "user_articulators": user_articulators,
        "user_articulators_texts": user_articulators_texts,
        "exercises": Exercise.objects.all(),
        "user_exercises": user_exercises,
        "user_exercises_texts": user_exercises_texts,
        "twisters": Twister.objects.all(),
        "user_twisters": user_twisters,
        "user_twisters_texts": user_twisters_texts,
    }


def build_exercises_pdf_response(context, base_dir):
    import os

    from django.utils.html import strip_tags
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="lingwolamkowe-cwiczenia.pdf"'

    font_path = os.path.join(
        base_dir,
        "tonguetwister",
        "static",
        "tonguetwister",
        "fonts",
        "arial.ttf",
    )
    pdfmetrics.registerFont(TTFont("Arial", font_path))

    pdf = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="PolishNormal", fontName="Arial", fontSize=12))
    styles.add(ParagraphStyle(name="PolishHeading", fontName="Arial", fontSize=14, spaceAfter=12))
    story = []

    story.append(Paragraph("Rozgrzewanie artykulatorów", styles["PolishHeading"]))
    for art in context["user_articulators_texts"]:
        story.append(Paragraph(strip_tags(art), styles["PolishNormal"]))
        story.append(Spacer(1, 12))

    story.append(Paragraph("Ćwiczenia właściwe", styles["PolishHeading"]))
    for exercise in context["user_exercises_texts"]:
        story.append(Paragraph(strip_tags(exercise), styles["PolishNormal"]))
        story.append(Spacer(1, 12))

    story.append(Paragraph("Łamańce językowe", styles["PolishHeading"]))
    for twister in context["user_twisters_texts"]:
        story.append(Paragraph(strip_tags(twister), styles["PolishNormal"]))
        story.append(Spacer(1, 12))

    pdf.build(story)
    return response
