from django.urls import path
from . import views

app_name = "bies"

urlpatterns = [
    path("", views.wyraj_lista, name="wyraj-lista"),
    path("swietowit-letni/", views.wyraj_swietowit_letni, name="wyraj-swietowit-letni"),
]