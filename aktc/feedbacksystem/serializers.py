
from .models import (Feedback, Review, 
                SupportTicket)
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth.models import User

from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db.models import Q, F, Sum


class FeedbackSerializer(serializers.ModelSerializer):

    from_location = serializers.CharField(
        source='trip_books.location_from.state', read_only=True)
    to_destination = serializers.CharField(
        source='trip_books.destination_to.state', read_only=True)
    departure_date = serializers.CharField(
        source='trip_books.departure_date', read_only=True)
    departure_time = serializers.CharField(
        source='trip_books.departure_time', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'rating',
                  'comment', 'trip_books', "from_location", "to_destination",
                  "departure_date", "departure_time", 'submitted_at']
        read_only_fields = ['submitted_at', 'user']

    def validate(self, data):
        trip_books = data['trip_books']
        if timezone.now() > trip_books.departure_date + timedelta(hours=48):
            raise serializers.ValidationError("Feedback window has expired.")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'email', 'rating', 'comment', 'submitted_at']
        read_only_fields = ['submitted_at']

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['id', 'name', 'email', 'subject',
                  'message', 'submitted_at', 'resolved']
