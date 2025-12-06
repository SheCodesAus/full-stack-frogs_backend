from django.urls import path
from . import views

urlpatterns = [
    path('teams/<int:pk>/', views.TeamDetail.as_view()),
    path('teams/', views.TeamList.as_view()),
    path('users/', views.CustomUserList.as_view()),
    path('users/<int:pk>/', views.CustomUserDetail.as_view()),
    path('me/', views.CustomUserMeView.as_view(), name='me'),
    path('send/', SendKudosView.as_view(), name='send-kudos'),
    path('dashboard/', dashboard, name='dashboard'),
    path('sent/', my_sent_kudos, name='sent-kudos'),
    path('team-all/', all_team_kudos, name='team-kudos'),
]