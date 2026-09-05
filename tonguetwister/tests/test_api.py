import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tonguetwister.models import Articulator, Exercise, Funfact, OldPolish, Trivia, Twister
from tonguetwister.serializers import (
    ArticulatorSerializer,
    ExerciseSerializer,
    FunfactSerializer,
    OldPolishSerializer,
    TriviaSerializer,
    TwisterSerializer,
)
from tonguetwister.throttling import AuthTokenThrottle, CustomAnonThrottle

# --- FIXTURES ---


@pytest.fixture
def api_client():
    """Return a DRF APIClient instance without authentication."""
    return APIClient()


@pytest.fixture
def auth_client():
    """Return a DRF APIClient instance authenticated via JWT token."""
    user = User.objects.create_user(username="testuser", password="pass123")
    token = RefreshToken.for_user(user).access_token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


# --- OLD POLISH ---


@pytest.mark.django_db
def test_oldpolish_list_success(api_client):
    """Should return a list with a single OldPolish object."""
    obj = OldPolish.objects.create(old_text="ćwiczenie", new_text="ćwiczenie")
    response = api_client.get("/tonguetwister/api/oldpolish/")
    assert response.status_code == 200
    assert response.data["results"] == OldPolishSerializer([obj], many=True).data


@pytest.mark.django_db
def test_oldpolish_list_not_found(api_client):
    """Should return an empty list when no matching search results."""
    response = api_client.get("/tonguetwister/api/oldpolish/?search=xyz")
    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []


@pytest.mark.django_db
def test_oldpolish_random_success(api_client):
    obj = OldPolish.objects.create(old_text="old_text", new_text="new_text")
    response = api_client.get("/tonguetwister/api/oldpolish/random/")
    assert response.status_code == 200
    assert response.data == OldPolishSerializer(obj).data


@pytest.mark.django_db
def test_oldpolish_random_empty_is_404(api_client):
    response = api_client.get("/tonguetwister/api/oldpolish/random/")
    assert response.status_code == 404
    assert response.data["detail"] == "No results found"


# --- ARTICULATORS ---


@pytest.mark.django_db
def test_articulator_list_success(api_client):
    """Should return a list with a single Articulator object."""
    obj = Articulator.objects.create(text="Szczebrzeszyn")
    response = api_client.get("/tonguetwister/api/articulators/")
    assert response.status_code == 200
    assert response.data["results"] == ArticulatorSerializer([obj], many=True).data


@pytest.mark.django_db
def test_articulator_list_not_found(api_client):
    """Should return an empty result when no Articulator matches."""
    response = api_client.get("/tonguetwister/api/articulators/?search=nieistnieje")
    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []


# --- TWISTERS ---


@pytest.mark.django_db
def test_twister_list_success(api_client):
    """Should return a list with a single Twister object."""
    obj = Twister.objects.create(text="Król Karol kupił królowej Karolinie korale")
    response = api_client.get("/tonguetwister/api/twisters/")
    assert response.status_code == 200
    assert response.data["results"] == TwisterSerializer([obj], many=True).data


@pytest.mark.django_db
def test_twister_list_not_found(api_client):
    """Should return an empty list when Twister is not found."""
    response = api_client.get("/tonguetwister/api/twisters/?search=xyz")
    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []


# --- EXERCISES ---


@pytest.mark.django_db
def test_exercise_list_success(api_client):
    """Should return a list with a single Exercise object."""
    obj = Exercise.objects.create(text="Ćwicz: szosa, susza")
    response = api_client.get("/tonguetwister/api/exercises/")
    assert response.status_code == 200
    assert response.data["results"] == ExerciseSerializer([obj], many=True).data


@pytest.mark.django_db
def test_exercise_list_not_found(api_client):
    """Should return an empty result when Exercise not found."""
    response = api_client.get("/tonguetwister/api/exercises/?search=xyz")
    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []


# --- TRIVIAS ---


@pytest.mark.django_db
def test_trivia_list_success(api_client):
    """Should return a list with a single Trivia object."""
    obj = Trivia.objects.create(text="Polski alfabet ma 32 litery")
    response = api_client.get("/tonguetwister/api/trivias/")
    assert response.status_code == 200
    assert response.data["results"] == TriviaSerializer([obj], many=True).data


@pytest.mark.django_db
def test_trivia_list_not_found(api_client):
    """Should return empty list for unmatched Trivia query."""
    response = api_client.get("/tonguetwister/api/trivias/?search=xyz")
    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []


# --- FUNFACTS (JWT protected) ---


@pytest.mark.django_db
def test_funfact_list_success(auth_client):
    """Should return a list of Funfacts for an authenticated user."""
    obj = Funfact.objects.create(text="W polskim są nosówki.")
    response = auth_client.get("/tonguetwister/api/funfacts/")
    assert response.status_code == 200
    assert response.data["results"] == FunfactSerializer([obj], many=True).data


@pytest.mark.django_db
def test_funfact_list_unauthorized(api_client):
    """Should deny access without JWT token."""
    response = api_client.get("/tonguetwister/api/funfacts/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_funfact_unauthorized_after_authenticated_request_stays_401():
    """Authenticated response must not be reused for anonymous caller."""
    user = User.objects.create_user(username="cache-user", password="pass123")
    token = RefreshToken.for_user(user).access_token
    auth_client = APIClient()
    auth_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    Funfact.objects.create(text="cache isolation check")

    first = auth_client.get("/tonguetwister/api/funfacts/")
    assert first.status_code == 200

    anon_client = APIClient()
    second = anon_client.get("/tonguetwister/api/funfacts/")
    assert second.status_code == 401


@pytest.mark.django_db
def test_funfact_list_not_found(auth_client):
    """Should return an empty list when no Funfacts match the search query."""
    response = auth_client.get("/tonguetwister/api/funfacts/?search=xyz")
    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []


# --- AUTH (JWT tokens) ---


@pytest.mark.django_db
def test_token_obtain_success(api_client):
    """Should issue JWT access and refresh tokens for valid credentials."""
    user = User.objects.create_user(username="testuser", password="pass123")
    user.profile.email_confirmed = True
    user.profile.save(update_fields=["email_confirmed"])
    response = api_client.post(
        "/tonguetwister/api/token/",
        data={"username": "testuser", "password": "pass123"},
    )
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_token_obtain_rejects_unconfirmed_email(api_client):
    User.objects.create_user(username="unconfirmed", password="pass123")
    unconfirmed = api_client.post(
        "/tonguetwister/api/token/",
        data={"username": "unconfirmed", "password": "pass123"},
    )
    invalid = api_client.post(
        "/tonguetwister/api/token/",
        data={"username": "missing", "password": "wrong"},
    )
    assert unconfirmed.status_code == 401
    assert invalid.status_code == 401
    assert unconfirmed.data == invalid.data
    assert "access" not in unconfirmed.data


@pytest.mark.django_db
def test_token_obtain_fail(api_client):
    """Should return 401 when login credentials are invalid."""
    response = api_client.post(
        "/tonguetwister/api/token/",
        data={"username": "wrong", "password": "wrong"},
    )
    assert response.status_code == 401


def test_token_views_use_auth_token_throttle():
    from tonguetwister.views_api import CustomTokenObtainPairView, CustomTokenRefreshView

    assert CustomAnonThrottle().get_rate() == "50/hour"
    assert AuthTokenThrottle().get_rate() == "5/min"
    assert CustomTokenObtainPairView.throttle_classes == [AuthTokenThrottle]
    assert CustomTokenRefreshView.throttle_classes == [AuthTokenThrottle]
