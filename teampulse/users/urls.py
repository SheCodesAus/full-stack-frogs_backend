from django.urls import path
from . import views

urlpatterns = [
    path('teams/<int:pk>/', views.TeamDetail.as_view()),
    path('teams/', views.TeamList.as_view()),
    path('users/', views.CustomUserList.as_view()),
    path('users/<int:pk>/', views.CustomUserDetail.as_view()),
    path('me/', views.CustomUserMeView.as_view(), name='me')
]