from django.urls import path

from . import views_api, views_auth, views_main

app_name = "poligon"

urlpatterns = [
    path("", views_main.home, name="home"),
    path("dashboard/", views_main.dashboard, name="dashboard"),
    path("practice/", views_main.practice, name="practice"),
    path("exercise/<slug:slug>/", views_main.exercise, name="exercise"),
    path("result/<int:submission_id>/", views_main.result, name="result"),
    path("reviews/", views_main.reviews, name="reviews"),
    path("reviews/<int:review_id>/grade/", views_main.grade_review, name="grade_review"),
    path("settings/", views_main.settings_view, name="settings"),
    path("poziom/", views_main.placement, name="placement"),
    path("sources/", views_main.sources, name="sources"),
    # Account: optional, only to keep progress
    path("konto/", views_auth.account, name="account"),
    path("konto/logowanie/", views_auth.login_view, name="login"),
    path("konto/wyloguj/", views_auth.logout_view, name="logout"),
    path("konto/rejestracja/", views_auth.register_view, name="register"),
    path("konto/aktywacja/<uidb64>/<token>/", views_auth.activate, name="activate"),
    path("konto/haslo/", views_auth.password_view, name="password"),
    path("konto/haslo/<uidb64>/<token>/", views_auth.password_set_view, name="password_set"),
    path("api/progress/", views_api.ProgressView.as_view(), name="api_progress"),
]
