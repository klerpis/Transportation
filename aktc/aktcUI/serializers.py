
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth.models import User
from setupsystem.serializers import DepartureTimeSerializer
from .models import (
    Booking, Location, PaymentMethod,
    BusDetail, Trip, Payment
)
from feedbacksystem.models import Feedback

from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db.models import Q, F, Sum


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class CUserserializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('title', 'name', 'reference',)



class BookingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    # booking_id = serializers.CharField(
    #     source="booking.booking_id", read_only=True)
    trip_id = serializers.CharField(
        source="booking.trip.trip_id", read_only=True)
    booking = BookingPaymentSerializer()
    method = PaymentMethodSerializer()

    class Meta:
        model = Payment
        fields = ['id', 'trip_id', 'booking', 
        'amount', 'method', 'status', 'reference', 'created']
        read_only_fields = ['id', 'booking_id', 'amount', 'status', 'created']


#     location_from = LocationSerializer(read_only=True)
#     destination_to = LocationSerializer(read_only=True)
#     departure_time = DepartureTimeSerializer(read_only=True)


class BookingCreateSerializer(serializers.ModelSerializer):
    # fare = serializers.DecimalField(
    #     max_digits=10, decimal_places=2, read_only=True)
    # location_from = serializers.SerializerMethodField()
    # destination_to = serializers.SerializerMethodField()
    # bus_detail = serializers.SerializerMethodField()
    # trip_id = serializers.CharField(write_only=True)

    # departure_time = DepartureTimeSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'email', 'booked_route', 'customer',
            'first_name', 'last_name', 'booking_id',
            'payment_due', 'status', 'feedback_resolved',
            'location_from', 'destination_to',
            'departure_date', 'departure_time',
            'num_of_pass', 'bus_detail'  # 'fare', 'id'  # 'bus_detail'
        ]

    # def get_trip(self, obj):
    #     return Trip.objects.filter(trip_id=obj.trip_id).first()

    # def get_bus_detail(self, obj):
    #     return BusDetail.objects.all().first()

    # def get_location_from(self, obj):
    #     return Location.objects.filter(bus_stop=obj.location_from).first()

    # def get_destination_to(self, obj):
    #     return Location.objects.filter(bus_stop=obj.destination_to).first()

    def create(self, validated_data):
        # print("Booking serializer print", validated_data, )
        print("Booking serializer print", validated_data.get('trip', 'nothing'))
        print("bus_detail", validated_data.get('bus_detail', 'no bus_detail'))
        print("destination_to", validated_data.get(
            'destination_to', 'no destination_to'))
        print("location_from", validated_data.get(
            'location_from', 'no location_from'))
        # print()
        booking = super().create(validated_data)
        print("Booking serializer print", booking)
        print()
        return booking

    def validate(self, data):
        # departure_date = data['departure_date']
        # num_of_pass = data['num_of_pass']
        # departure_time = data['departure_time']
        # bus_detail = data['bus_detail']

        # Weekday check
        # selected_day = departure_date.weekday()  # 0 = Monday
        # if str(selected_day) != str(bus_detail.weekday.weekday_number):
        #     raise serializers.ValidationError("Bus does not run on this day.")

        # Seat check
        # current_booked = Booking.objects.filter(
        #     # bus_detail=bus_detail,
        #     departure_date=departure_date,
        #     departure_time=departure_time
        # ).aggregate(total=Sum('num_of_pass'))['total'] or 0

        # available_seats = bus_detail.bus.total_seat - current_booked
        # if num_of_pass > available_seats:
        #     raise serializers.ValidationError(
        #         f"Only {available_seats} seats available.")

        return data


# serializers.py
class BookingListSerializer(serializers.ModelSerializer):
    # bus = serializers.CharField(
    #     source='bus_detail.bus.bus_number', read_only=True)
    # driver = serializers.CharField(
    #     source='bus_detail.driver.driver_name', read_only=True)
    from_location = serializers.CharField(
        source='location_from.state', read_only=True)
    to_location = serializers.CharField(
        source='destination_to.state', read_only=True)
    from_local_gov = serializers.CharField(
        source='location_from.local_government', read_only=True)
    to_local_gov = serializers.CharField(
        source='destination_to.local_government', read_only=True)
    from_bus_stop = serializers.CharField(
        source='location_from.bus_stop', read_only=True)
    to_bus_stop = serializers.CharField(
        source='destination_to.bus_stop', read_only=True)
    from_street = serializers.CharField(
        source='location_from.street', read_only=True)
    to_street = serializers.CharField(
        source='destination_to.street', read_only=True)

    fare = serializers.CharField(
        source='trip.trip_fare', read_only=True)
    feedback_submitted = serializers.SerializerMethodField()
    feedback_deadline = serializers.SerializerMethodField()
    isUpcoming = serializers.SerializerMethodField()
    

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_id', 'from_location', 'to_location', 'departure_date',
            'from_local_gov', 'to_local_gov', 'from_bus_stop', 'to_bus_stop',
            'from_street', 'to_street', 'departure_time', 'num_of_pass',
            'book_created_at', 'status', 'fare', 'trip', 'feedback_submitted',
            'feedback_resolved', 'feedback_deadline', 'isUpcoming',
        ]

    # def get_fare(self, obj):
    #     fare = getattr(obj.bus_detail.bus, 'fare', None)
    #     if fare:
    #         return fare * obj.num_of_pass
    #     return None

    def get_feedback_submitted(self, obj):
        # Feedback.objects.filter(trip_books=obj).exists()
        return Feedback.objects.filter(trip_books=obj).exists()

    def get_feedback_deadline(self, obj):
        return obj.departure_date + timedelta(days=1, hours=12)

    def get_isUpcoming(self, obj):
        str_format = '%H:%M%p'
        departure_time = datetime.strptime(
            obj.departure_time, str_format).time()
        departure_date_time = timezone.make_aware(
            datetime.combine(obj.departure_date, departure_time))
        return departure_date_time > now()


class BusDetailSerializer(serializers.ModelSerializer):
    driver = serializers.StringRelatedField()
    bus = serializers.StringRelatedField()
    weekday = serializers.StringRelatedField()
    daily_schedule = DepartureTimeSerializer(many=True)

    class Meta:
        model = BusDetail
        fields = ['id', 'bus', 'driver', 'weekday', 'daily_schedule']


class TripSerializer(serializers.ModelSerializer):
    from_location = serializers.CharField(
        source='route.from_location.bus_stop', read_only=True)
    to_location = serializers.CharField(
        source='route.to_destination.bus_stop', read_only=True)
    fare_per_seat = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = [
            'trip_id',
            # 'route',
            'from_location',
            'to_location',
            'trip_departure_date',
            'trip_departure_time',
            'status',
            'fare_per_seat',
        ]

    def get_fare_per_seat(self, obj):
        return obj.route.fare  # Assuming Route has a fare field


