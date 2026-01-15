from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Reward(models.Model):
    points = models.IntegerField(default=0)
    name = models.CharField(max_length=200)

class UserPoint(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='user_points',
        on_delete=models.CASCADE
    )
    points = models.IntegerField(default=0)
