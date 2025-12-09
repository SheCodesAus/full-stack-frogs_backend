from rest_framework import serializers
from django.apps import apps
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Call the base class __init__ method to set up all fields
        super().__init__(*args, **kwargs)

        # Logic to check if we are in a 'create' (POST) scenario
        # self.instance is None when a new object is being created
        if self.instance is None:
            # Explicitly set these fields as required only for creation
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
        # For updates (self.instance is not None), the fields default to
        # the requirements defined by the model (or the Meta extra_kwargs below),
        # making them optional for PUT/PATCH.

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': { 'write_only': True },
            'first_name': {
                # Ensure the field is not just an empty string, even when optional
                'allow_blank': False
                # Removed 'required': True here, as it's now handled conditionally in __init__
                },
            'last_name': {
                'allow_blank': False
                # Removed 'required': True here
                }
            }     #kwargs - keyword arguments #one cannot read password

    def create(self, validated_data): #validated - once serializers validate data, it will pass them into function so that it is ensured the data are valid

        return CustomUser.objects.create_user(**validated_data)

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('users.Team')
        fields = '__all__'