from django.urls import path

from . import views

app_name = "bies"

urlpatterns = [
    path("", views.wyraj_lista, name="wyraj-lista"),
    path("<slug:slug>/", views.wyraj_detail, name="wyraj-detail"),
]
