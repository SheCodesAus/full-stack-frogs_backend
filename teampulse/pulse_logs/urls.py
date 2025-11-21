from django.urls import path
from . import views

urlpatterns = [
    path('moods/', views.MoodList.as_view())
]