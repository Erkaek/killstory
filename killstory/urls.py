"""Routes."""

from django.urls import path

from . import views

app_name = "killstory"

urlpatterns = [
    path('', views.killstory_view, name='index'),  # Nommer la vue d'index pour l'application
    path('kill/<int:killmail_id>/', views.kill_detail_view, name='kill_detail'),
]
