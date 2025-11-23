from django.urls import path
from . import views

urlpatterns = [
    path('moods/', views.MoodList.as_view()),
    path('workloads/', views.WorkloadList.as_view())
]