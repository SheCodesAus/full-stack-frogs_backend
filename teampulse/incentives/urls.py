from django.urls import path
from . import views

urlpatterns = [
    path('rewards/', views.RewardList.as_view()),

]