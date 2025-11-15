from django.db import models
from django.contrib.auth import get_user_model

class PulseLog(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='logged_pulses',
        on_delete=models.CASCADE
    )
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
    workload = models.ForeignKey('Workload', on_delete=models.CASCADE)
    comment = models.TextField()
    # Team is not linked to Team model as it's write-only
    team = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Mood(models.Model):
    value = models.IntegerField()
    description = models.CharField(max_length=255)
    image_url = models.URLField()

class Workload(models.Model):
    value = models.IntegerField()
    description = models.CharField(max_length=255)
    image_url = models.URLField()