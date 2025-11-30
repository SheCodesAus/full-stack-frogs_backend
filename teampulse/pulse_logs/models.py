from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime

class PulseLog(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='logged_pulses',
        on_delete=models.CASCADE
    )
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
    workload = models.ForeignKey('Workload', on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    # Team is not linked to Team model as it's write-only
    team = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    timestamp_local = models.DateTimeField(null=True)

class Mood(models.Model):
    value = models.IntegerField()
    description = models.CharField(max_length=255)
    image_url = models.URLField()

class Workload(models.Model):
    value = models.IntegerField()
    description = models.CharField(max_length=255)
    image_url = models.URLField()