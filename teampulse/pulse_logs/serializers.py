from rest_framework import serializers
from django.apps import apps

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('pulse_logs.Mood')
        fields = '__all__'