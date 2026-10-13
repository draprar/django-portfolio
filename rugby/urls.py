from django.urls import path

from analytics.utils import count_visit

from . import views

urlpatterns = [
    path("", count_visit(views.post_list), name="post_list"),
]
