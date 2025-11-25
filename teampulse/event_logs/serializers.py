from rest_framework import serializers
from django.apps import apps

class EventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('event_logs.EventLog')
        fields = '__all__'