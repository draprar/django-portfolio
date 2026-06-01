from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from rest_framework import filters, serializers, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Articulator, Exercise, Funfact, OldPolish, Trivia, Twister
from .serializers import (
    ArticulatorSerializer,
    ExerciseSerializer,
    FunfactSerializer,
    OldPolishSerializer,
    TriviaSerializer,
    TwisterSerializer,
)

CACHE_TIMEOUT = 60 * 5  # 5 min

SEARCH_QUERY_PARAM = OpenApiParameter(
    name="search",
    type=str,
    location=OpenApiParameter.QUERY,
    description="Search query",
)


class _CachedSearchListMixin:
    @method_decorator(cache_page(CACHE_TIMEOUT, cache="default"))
    @extend_schema(parameters=[SEARCH_QUERY_PARAM])
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response if response.data else Response({"detail": "No results found"}, status=404)


class OldPolishViewSet(_CachedSearchListMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Old Polish phrases with modern translations.

    Provides read-only access to historical Polish phrases and their modern equivalents.
    Useful for language learners interested in etymology and historical language context.

    Supported query parameters:
    - search: Search query to filter by old_text or new_text (cached for 5 minutes)

    Permissions: Public (no authentication required)
    """

    queryset = OldPolish.objects.all()
    serializer_class = OldPolishSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["old_text", "new_text"]
    permission_classes = [AllowAny]


class ArticulatorViewSet(_CachedSearchListMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for articulators and pronunciation guides.

    Provides read-only access to articulator content used for pronunciation practice.
    Results are cached for 5 minutes to improve performance.

    Supported query parameters:
    - search: Search query to filter by text content

    Permissions: Public (no authentication required)
    """

    queryset = Articulator.objects.all()
    serializer_class = ArticulatorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["text"]
    permission_classes = [AllowAny]


class FunfactViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for fun facts about language and pronunciation.

    Provides read-only access to interesting facts and trivia.
    Content is related to language learning and practice.

    Supported query parameters:
    - search: Search query to filter by text content

    Permissions: Authenticated users only (requires valid JWT token)

    To access:
    1. Obtain JWT token via /api/token/
    2. Include in request header: Authorization: Bearer <token>
    """

    queryset = Funfact.objects.all()
    serializer_class = FunfactSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["text"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class TwisterViewSet(_CachedSearchListMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for tongue twisters.

    Provides read-only access to tongue twister content for pronunciation practice.
    Results are cached for 5 minutes.

    Supported query parameters:
    - search: Search query to filter by text content

    Permissions: Public (no authentication required)
    """

    queryset = Twister.objects.all()
    serializer_class = TwisterSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["text"]
    permission_classes = [AllowAny]


class ExerciseViewSet(_CachedSearchListMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for language exercises.

    Provides read-only access to pronunciation and articulation exercises.
    Results are cached for 5 minutes for better performance.

    Supported query parameters:
    - search: Search query to filter by text content

    Permissions: Public (no authentication required)
    """

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["text"]
    permission_classes = [AllowAny]


class TriviaViewSet(_CachedSearchListMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for language trivia and interesting facts.

    Provides read-only access to trivia content related to language and linguistics.
    Results are cached for 5 minutes.

    Supported query parameters:
    - search: Search query to filter by text content

    Permissions: Public (no authentication required)
    """

    queryset = Trivia.objects.all()
    serializer_class = TriviaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["text"]
    permission_classes = [AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    API endpoint to obtain JWT authentication tokens.

    POST /api/token/

    Request body:
    {
        "username": "user@example.com or username",
        "password": "password"
    }

    Response:
    {
        "access": "<JWT access token>",
        "refresh": "<JWT refresh token>"
    }

    Usage:
    1. Send POST with credentials to get tokens
    2. Use 'access' token in Authorization header: Authorization: Bearer <access>
    3. Access token valid for 30 minutes
    4. Use 'refresh' token to obtain new access token

    Permissions: Public (no authentication required)
    """

    @extend_schema(
        tags=["Authentication"],
        summary="Zaloguj i pobierz token JWT",
        description="Podaj login i hasło, aby otrzymać JWT access i refresh token.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class HealthCheckView(APIView):
    """
    API health check endpoint.

    GET /api/health/

    Response:
    {
        "status": "ok"
    }

    Used for monitoring and load balancer health checks.
    Always returns 200 OK if the service is running.

    Permissions: Public (no authentication required)
    """

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Health"],
        responses={
            200: inline_serializer(
                name="HealthCheckResponse",
                fields={"status": serializers.CharField()},
            )
        },
    )
    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"}, status=200)
