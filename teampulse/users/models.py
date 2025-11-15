from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

class Team(models.Model):
    team_name = models.CharField(max_length=200)