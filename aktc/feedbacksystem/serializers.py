
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

from aktcUI.models import Booking, Customer

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
        fields = ['user', 'rating', 
                  'comment', "from_location", "to_destination",
                  "departure_date", "departure_time", 'submitted_at']
        read_only_fields = ['submitted_at', 'user']

    def validate(self, data):

        print()
        print()
        # print("data", data, self.validated_data)
        print()
        print("data", data, self.initial_data)
        print()
        print("data", data, self.initial)
        print()
        print("data", dir(self))
        print()
        print("self", self.context['request'].user)
        print()
        print("self", self.instance, self.get_extra_kwargs)
        print()

        departure_date = self.initial_data['departureDate']
        departure_time = self.initial_data['departureTime']
        booking_id = self.initial_data['booking']
        
        joined_date = f"{departure_date} {departure_time}"
        joined_date = datetime.strptime(joined_date, "%Y-%m-%d %H:%M%p")

        feedback_departure_datetime = timezone.make_aware(joined_date)

        if timezone.now() > feedback_departure_datetime + timedelta(hours=48):
            raise serializers.ValidationError("Feedback window has expired.")
        booking = Booking.objects.filter(booking_id=booking_id).first()
        data['trip_books'] = booking
        user = self.context['request'].user
        customer = Customer.objects.filter(user=user).first()
        data['user'] = customer
        print(booking, customer)
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
