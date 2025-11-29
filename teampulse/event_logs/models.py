from django.db import models

class EventLog(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    event_name = models.CharField(max_length=200)
    version = models.IntegerField()
    metadata = models.JSONField(null=True)