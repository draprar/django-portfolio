from django.urls import path

from .views import WybierzView

app_name = "rozdroze"

urlpatterns = [
    path("", WybierzView.as_view(), name="wybierz"),
]
