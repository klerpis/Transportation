from rest_framework import serializers
from .models import Profile
from aktcUI.models import Customer
from django.contrib.auth import get_user_model


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    firstname = serializers.CharField(
        source='user.first_name')
    lastname = serializers.CharField(source='user.last_name')
    has_admin_status = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['email', 'username', 'firstname', 'has_admin_status',
                  'lastname', 'phonenumber', 'bio', 'avatar']

    def get_has_admin_status(self, obj):
        # print("SEPER USER SELF", self, obj)
        print("SEPER USER iducbjhs ", dir(obj.user))
        return obj.user.is_staff

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

        customer = Customer.objects.filter(user=user).first()
        customer.firstname =  firstname
        customer.surname =  lastname
        customer.email =  user_data.get('email', user.email)

        customer.save()

        user_data = {
            **validated_data,
            'email': user_data.get('email', user.email),
        }

        # Now update profile fields normally
        return super().update(instance, user_data)



#!/usr/bin/env bash

# # Exit on error
# set -o errexit

# # 1. Install dependencies
# pip install -r requirements.txt

# # 2. Apply database migrations
# python manage.py migrate

# # 3. Collect static files
# python manage.py collectstatic --noinput

# # 4. Optional: Load initial data (if needed and db.json is committed)
# python manage.py loaddata db.json

# # 5. Optional: Compile translation messages
# # python manage.py compilemessages
