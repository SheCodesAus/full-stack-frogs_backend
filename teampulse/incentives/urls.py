from django.urls import path
from . import views

urlpatterns = [
    path('rewards/', views.RewardList.as_view()),
    path('rewards/<int:pk>/', views.RewardDetail.as_view()),
    path('user_points/', views.UserPointList.as_view()),
    path('user_points/<int:pk>/', views.UserPointDetail.as_view(), name='user_point_detail')

]