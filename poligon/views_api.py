from django.utils import timezone
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .identity import learner_state
from .models import Review, Submission
from .serializers import ProgressSerializer
from .services import skill_scores


@method_decorator(ratelimit(key="ip", rate="30/m", method="GET", block=True), name="dispatch")
class ProgressView(APIView):
    """Session-scoped training progress. Anonymous visitors get their own row."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    throttle_classes: list = []

    @extend_schema(responses=ProgressSerializer, tags=["Poligon"])
    def get(self, request: Request) -> Response:
        state = learner_state(request)
        submissions = Submission.objects.filter(learner=state).select_related("exercise")
        payload = {
            "target_profile": state.target_profile,
            "scores": skill_scores(submissions),
            "submissions": submissions.count(),
            "due_reviews": Review.objects.filter(
                learner=state,
                due_at__lte=timezone.now(),
            ).count(),
        }
        return Response(ProgressSerializer(payload).data)
