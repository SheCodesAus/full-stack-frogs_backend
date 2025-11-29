from rest_framework import serializers
from django.apps import apps
from .models import CustomUser

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