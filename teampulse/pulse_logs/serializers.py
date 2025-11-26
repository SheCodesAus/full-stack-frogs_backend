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
    year = serializers.SerializerMethodField()
    week_index = serializers.SerializerMethodField()
    year_week = serializers.SerializerMethodField()

    class Meta:
        model = apps.get_model('pulse_logs.PulseLog')
        fields = '__all__'

    def get_year(self, obj):
        # Assuming 'timestamp' or 'timestamp_local' is the field on the model
        if obj.timestamp_local:
            return obj.timestamp_local.year
        return 0

    def get_week_index(self, obj):
        if obj.timestamp_local:
            # Use %V to get the ISO 8601 week number
            return int(obj.timestamp_local.strftime("%V"))
        return 0

    def get_year_week(self, obj):
        if obj.timestamp_local:
            year = (self.get_year(obj) * 100) + self.get_week_index(obj)
            return year
        return 0