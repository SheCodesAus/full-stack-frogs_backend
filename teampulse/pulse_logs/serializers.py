from rest_framework import serializers
from django.apps import apps
from django.contrib.auth import get_user_model

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
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    # Make these fields optional for the user, so they can be calculated automatically on creation
    # but still updated manually if needed later.
    year = serializers.IntegerField(required=False)
    week_index = serializers.IntegerField(required=False)
    year_week = serializers.IntegerField(required=False)

    class Meta:
        model = apps.get_model('pulse_logs.PulseLog')
        fields = '__all__'
        read_only_fields = ('user', 'timestamp')

class PulseLogDetailSerializer(PulseLogSerializer):

    # Redefine user to be writable for updates
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        required=False
    )

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.team = validated_data.get('team', instance.team)
        instance.mood = validated_data.get('mood', instance.mood)
        instance.workload = validated_data.get('workload', instance.workload)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.timestamp = instance.timestamp
        instance.timestamp_local = validated_data.get('timestamp_local', instance.timestamp_local)
        instance.year = validated_data.get('year', instance.year)
        instance.week_index = validated_data.get('week_index', instance.week_index)
        instance.year_week = validated_data.get('year_week', instance.year_week)
        instance.save()
        return instance