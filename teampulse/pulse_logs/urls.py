from django.urls import path
from . import views

urlpatterns = [
    path('moods/<int:pk>/', views.MoodDetail.as_view()),
    path('moods/', views.MoodList.as_view()),
    path('workloads/', views.WorkloadList.as_view()),
    path('pulse_logs/', views.PulseLogList.as_view(), name='pulse_logs'),
    path('pulse_logs/<int:pk>/', views.PulseLogDetail.as_view(), name='pulse_log_detail')
]