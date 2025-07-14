from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    firstname = serializers.CharField(
        source='user.first_name')
    lastname = serializers.CharField(source='user.last_name')

    class Meta:
        model = Profile
        fields = ['email', 'username', 'firstname',
                  'lastname', 'phonenumber', 'bio', 'avatar']

    def update(self, instance, validated_data):
        # Extract and pop user-related fields
        firstname = validated_data.pop('firstname', '')
        lastname = validated_data.pop('lastname', '')
        username = validated_data.pop('username', '')
        user_data = validated_data.pop('user', {})

        # Update user fields manually
        user = instance.user
        user.email = user_data.get('email', user.email)

        user.username = firstname or user_data.get('username', user.username)
        user.first_name = lastname or user_data.get(
            'first_name', user.first_name)
        user.last_name = username or user_data.get('last_name', user.last_name)

        # user.username = user_data.get('username', user.username)
        # user.first_name = user_data.get('first_name', user.first_name)
        # user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        # Now update profile fields normally
        return super().update(instance, validated_data)
