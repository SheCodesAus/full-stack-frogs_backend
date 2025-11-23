from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.TeamList.as_view())
]