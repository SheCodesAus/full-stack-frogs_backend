from rest_framework import serializers
from django.apps import apps

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('pulse_logs.Mood')
        fields = '__all__'

class WorkloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('pulse_logs.Workload')
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('users.Team')
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('users.CustomUser')
        fields = '__all__'