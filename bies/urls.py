from django.urls import path
from . import views

app_name = "bies"

urlpatterns = [
    path("", views.wyraj_lista, name="wyraj-lista"),
    path("swietowit-letni/", views.wyraj_swietowit_letni, name="wyraj-swietowit-letni"),
    path("gaik/", views.wyraj_gaik, name="wyraj-gaik"),
    path("radonica/", views.wyraj_radonica, name="wyraj-radonica"),
    path("smigus-dyngus/", views.wyraj_smigus_dyngus, name="wyraj-smigus-dyngus"),
    path("jare-gody/", views.wyraj_jare_gody, name="wyraj-jare-gody"),
    path("miesopust/", views.wyraj_miesopust, name="wyraj-miesopust"),
    path("szczodre-gody/", views.wyraj_szczodre_gody, name="wyraj-szczodre-gody"),
]
