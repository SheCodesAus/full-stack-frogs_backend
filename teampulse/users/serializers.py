from rest_framework import serializers
from django.apps import apps
from .models import CustomUser, Kudos

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': { 'write_only': True }}     #kwargs - keyword arguments #one cannot read password

    def create(self, validated_data): #validated - once serializers validate data, it will pass them into function so that it is ensured the data are valid

        return CustomUser.objects.create_user(**validated_data)

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('users.Team')
        fields = '__all__'

class KudosSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('users.Kudos')
        fields = '__all__'

class KudosDisplaySerializer(serializers.ModelSerializer):

    sender = CustomUserSerializer(read_only=True)
    recipient = CustomUserSerializer(read_only=True)

    class Meta:
        model = Kudos
        fields = [
            'id',
            'sender',          # shows sender's username, first_name, etc.
            'recipient',       # shows recipient's info
            'message',
            'timestamp',
            'is_acknowledged'             # True/False — shows if recipient has read it
        ]