from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

class Team(models.Model):
    team_name = models.CharField(max_length=200)
    team_manager = models.IntegerField(null=True)

class Kudos(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,            # prevent deleting user if they sent kudos
        related_name='sent_kudos',
        null = True,
        blank = True
    )
    recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='received_kudos',
        null = True,
        blank = True
    )
    message = models.TextField(null=True)
    is_acknowledged = models.BooleanField(default=False)
