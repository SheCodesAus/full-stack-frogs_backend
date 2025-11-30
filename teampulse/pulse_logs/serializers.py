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

class PulseLogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    # Make these fields optional for the user, so they can be calculated automatically on creation
    # but still updated manually if needed later.
    year = serializers.IntegerField(required=False)
    week_index = serializers.IntegerField(required=False)
    year_week = serializers.IntegerField(required=False)

    class Meta:
        model = apps.get_model('pulse_logs.PulseLog')
        fields = '__all__'
        read_only_fields = ('user', 'timestamp')
