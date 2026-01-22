from rest_framework import serializers
from django.apps import apps
from django.contrib.auth import get_user_model

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('incentives.Reward')
        fields = '__all__'

class UserPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('incentives.UserPoint')
        fields = '__all__'