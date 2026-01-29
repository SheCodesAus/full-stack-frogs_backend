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
        on_delete=models.SET_NULL,  # Changed: Set to NULL instead of cascading delete
        related_name='sent_kudos',
        null=True,  # Allow NULL to preserve Kudos when user is deleted
        default=None  # Explicit default for new records and migrations
    )
    sender_first_name = models.CharField(max_length=200, blank=True, default='')
    sender_last_name = models.CharField(max_length=200, blank=True, default='')
    recipient = models.IntegerField()
    message = models.TextField(null=True)
    is_acknowledged = models.BooleanField(default=False)
