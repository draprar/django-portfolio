from django.urls import path

from . import views, views_api

app_name = "walczak"

urlpatterns = [
    path("", views.home, name="home"),
    path("spis/", views.style_list, name="list"),
    path("spis/<slug:slug>/", views.style_detail, name="detail"),
    path("test/", views.preference_test, name="test"),
    path("dopasowanie/", views.preference_result, name="match"),
    path("porownaj/", views.compare_form, name="compare_form"),
    path("porownaj/<slug:a>/<slug:b>/", views.compare, name="compare"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("api/martial-arts/", views_api.MartialArtListView.as_view(), name="api-styles"),
    path("api/martial-arts/<slug:slug>/", views_api.MartialArtDetailView.as_view(), name="api-style"),
    path("api/tags/", views_api.TagListView.as_view(), name="api-tags"),
    path("api/random-fact/", views_api.RandomFactView.as_view(), name="api-fact"),
]
