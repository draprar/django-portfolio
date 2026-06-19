from django.urls import path

from . import views

app_name = "bies"

urlpatterns = [
    # Lista wszystkich świąt
    path("", views.wyraj_lista, name="wyraj-lista"),

    # Szczegół święta — jeden wzorzec zamiast 7 osobnych
    # np. /wyraj/gaik/  /wyraj/jare-gody/  /wyraj/szczodre-gody/
    path("<slug:slug>/", views.wyraj_detail, name="wyraj-detail"),
]
