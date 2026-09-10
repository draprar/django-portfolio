from django.urls import path

from .views import CodeView

app_name = "code"

urlpatterns = [
    path("", CodeView.as_view(), name="index"),
]
