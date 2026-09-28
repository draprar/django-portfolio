from django.utils import timezone
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .identity import account_state, current_plan
from .models import Review, Submission
from .serializers import ProgressSerializer
from .services import skill_scores


@method_decorator(ratelimit(key="ip", rate="30/m", method="GET", block=True), name="dispatch")
class ProgressView(APIView):
    """Training progress. Only an account has any: a guest is always at zero."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    throttle_classes: list = []

    @extend_schema(responses=ProgressSerializer, tags=["Poligon"])
    def get(self, request: Request) -> Response:
        plan = current_plan(request)
        state = account_state(request)
        submissions = (
            Submission.objects.filter(learner=state).select_related("exercise")
            if state is not None
            else Submission.objects.none()
        )
        payload = {
            "target_profile": plan.target_profile if plan else "2222",
            "scores": skill_scores(submissions),
            "submissions": submissions.count(),
            "due_reviews": (
                Review.objects.filter(learner=state, due_at__lte=timezone.now()).count()
                if state is not None
                else 0
            ),
        }
        return Response(ProgressSerializer(payload).data)
