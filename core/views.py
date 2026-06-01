import logging

from django.conf import settings
from django.db import DatabaseError
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views import View
from django_ratelimit.decorators import ratelimit

from .email import send_brevo_email
from .forms import ContactForm
from .models import Project

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Health check endpoint for monitoring and deployment verification.

    Returns:
        JsonResponse: {"status": "ok"} with 200 status code if backend is running.

    Args:
        request: HttpRequest object

    Use case: Called by monitoring services (e.g., Render, health probes) to verify
    the application is responsive.
    """
    return JsonResponse({"status": "ok"})


class HomeView(View):
    """
    Main portfolio page view.

    - Loads all projects from database
    - Renders contact form for user submissions
    - Gracefully handles database unavailability to keep homepage online

    Security:
    - Database errors are caught and logged without exposing details to users
    - Projects list degrades to empty list if database is temporarily down
    - Maintains service availability (fail-open approach)
    """

    template_name = "core/index.html"

    def get(self, request):
        form = ContactForm()
        # Keep homepage available even if DB is temporarily unavailable.
        try:
            projects = list(Project.objects.all())
        except DatabaseError:
            logger.exception("Failed to load projects for home page")
            projects = []
        return render(request, self.template_name, {"form": form, "projects": projects})


@method_decorator(ratelimit(key="ip", rate="5/m", block=True), name="dispatch")
class ContactView(View):
    """
    Secure contact endpoint:
    - rate-limited (5 requests/min per IP) via django-ratelimit
    - only POST accepted (GET/others → 405 via http_method_names)
    - rejects non-AJAX requests (X-Requested-With)
    - simple honeypot check for hidden 'website' field
    - does not log PII or message body
    """

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        # Basic XHR check (case-insensitive)
        if request.headers.get("x-requested-with", "").lower() != "xmlhttprequest":
            logger.warning(
                "Contact attempt rejected: missing or invalid XHR header from %s", request.META.get("REMOTE_ADDR")
            )
            return JsonResponse({"success": False, "message": "Invalid request."}, status=400)

        # Honeypot: invisible field that bots often fill
        if request.POST.get("website"):
            logger.warning("Honeypot triggered from %s", request.META.get("REMOTE_ADDR"))
            # Return a generic validation error without exposing details.
            return JsonResponse({"success": False, "message": "Invalid form data."}, status=400)

        form = ContactForm(request.POST)
        is_valid = form.is_valid()

        # Log only IP and validation result. Do NOT log form data or message content.
        logger.debug("Contact form submitted from %s. Valid: %s", request.META.get("REMOTE_ADDR"), is_valid)

        if not is_valid:
            errors = {field: list(errs) for field, errs in form.errors.items()}
            logger.warning("Invalid contact form from %s. Errors: %s", request.META.get("REMOTE_ADDR"), errors)
            return JsonResponse({"success": False, "message": "Invalid form data.", "errors": errors}, status=400)

        # At this point form is valid. Save and send email.
        try:
            # Persist (but avoid logging saved content)
            form.save()

            subject = "Kontakt"
            # Build email body from cleaned_data. We must include the message in the mail,
            # but do not log the content anywhere.
            name = form.cleaned_data.get("name", "Unknown")
            email = form.cleaned_data.get("email", "")
            message_body = form.cleaned_data.get("message", "")

            safe_message = escape(message_body).replace("\n", "<br>")

            html_content = f"""
                <p><strong>Message from:</strong> {escape(name)}</p>
                <p><strong>Email:</strong> {escape(email)}</p>
                <p>{safe_message}</p>
            """

            recipient_list = [settings.DEFAULT_FROM_EMAIL]

            result = send_brevo_email(subject, html_content, recipient_list)

            if result:
                logger.info("Contact form processed successfully from %s", request.META.get("REMOTE_ADDR"))
                return JsonResponse({"success": True, "message": "Your message has been sent successfully!"})
            else:
                logger.error("Email sending failed for contact from %s", request.META.get("REMOTE_ADDR"))
                return JsonResponse(
                    {"success": False, "message": "Email service failed, please try again later."}, status=500
                )

        except Exception:
            # logger.exception records traceback but avoid attaching user content
            logger.exception("Unhandled error processing contact form from %s", request.META.get("REMOTE_ADDR"))
            return JsonResponse(
                {"success": False, "message": "An error occurred while sending the email. Please try again later."},
                status=500,
            )
