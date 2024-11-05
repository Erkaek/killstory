"""Routes."""

from django.urls import path

from . import views

app_name = "killstory"

urlpatterns = [
    path("", views.index, name="index"),
]
