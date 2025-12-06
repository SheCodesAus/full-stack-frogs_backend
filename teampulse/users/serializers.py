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

class KudosCreateSerializer(serializers.ModelSerializer):
    recipient = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Kudos
        fields = ['recipient', 'message']

    def validate(self, data):
        sender = self.context['request'].user
        recipient = data['recipient']

        if sender == recipient:
            raise serializers.ValidationError("You cannot send kudos to yourself.")

        return data

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

class KudosDisplaySerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)
    recipient = CustomUserSerializer(read_only=True)

    class Meta:
        model = Kudos
        fields = ['id', 'sender', 'recipient', 'message', 'timestamp', 'is_acknowledged']