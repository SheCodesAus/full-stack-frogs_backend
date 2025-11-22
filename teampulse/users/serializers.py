from rest_framework import serializers
from .models import Team

class TeamSerializer(serializers.TeamSerializer):
    class Meta:
        model = apps.get_model('users.Team')
        fields = '__all__'