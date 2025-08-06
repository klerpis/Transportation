from django.db.models.signals import m2m_changed
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import random
import uuid
import datetime
from datetime import timedelta
# from functools import partial
from django.db import models
from django.conf import settings
from django.utils import timezone
# from django.db import DataError
from django.core import checks, exceptions, validators
from django.utils.translation import gettext_lazy as _
# from django.contrib.admin.templates import admin
# from django.contrib.auth import get_user_model

from setupsystem.models import Route, Location, WeekDaysSchedule

# User = get_user_model()

class Customer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Customer's Name", on_delete=models.CASCADE,
        null=True, blank=True)
    firstname = models.CharField(max_length=45)
    middlename = models.CharField(max_length=45, null=True, blank=True)
    surname = models.CharField(max_length=45, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return f"{self.firstname}  || {self.email} "




class Driver(models.Model):
    driver_name = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Driver's Name", 
        on_delete=models.CASCADE)
    driver_phonenumber = models.CharField(
        "Driver's Phone Number", max_length=18, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    passport = models.ImageField(upload_to='passport', null=True, blank=True)  # not compulsory yet
    known_routes = models.ManyToManyField(
        Route, related_name='known_routes', blank=True)
    current_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True)  # to aid the auto scheduling algorithm
    # current_roster_location = models.ForeignKey(
    #     Location, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.driver_name} || Email: {self.email}'


class Bus(models.Model):

    class Meta:
        verbose_name = 'Bus'
        verbose_name_plural = 'Bus List'

    BUS_STATUS_CHOICES = [
        ("RN", "Running"),
        ("DW", "Down"),
    ]
    registration_number = models.CharField(max_length=40)
    bus_name = models.CharField(max_length=20, default='company bus new')
    bus_seat_num = models.PositiveIntegerField(default=1)
    bus_status = models.CharField(
        choices=BUS_STATUS_CHOICES, default=BUS_STATUS_CHOICES[0][1])

    def __str__(self):
        return f'{self.bus_name} || {self.registration_number}'


class BusDetail(models.Model):
    # for now busdetails will only be used in bookings not trip
    # until the algorithm for driver roster is develop (which as of now is beyond me)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    bus_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL,
                                   blank=True, null=True)

    def __str__(self):
        self.return_ = f'''
            {self.bus.bus_name} || {self.bus.registration_number} || {self.bus.bus_status} || 
            '''
        return self.return_

def generate_trip_id():
    date_part = datetime.date.today().strftime("%Y%m%d%H%M%S%p%j")
    random_part = uuid.uuid4().hex[:5].upper()
    return f"TRIP-{date_part}-{random_part}"


class Trip(models.Model):

    class Meta:
        verbose_name = 'Scheduled Trip'
        verbose_name_plural = 'Scheduled Trips'

    TRIP_STATUS_CHOICES = [("pending", "Pending"), ("started", "Started"),
                           ("completed", "Completed"), ("cancelled", "Cancelled")]


    # leave blank
    trip_id = models.CharField(
        max_length=40, unique=True, editable=False, blank=True)

    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField(default=0)  # management side
    trip_departure_date = models.CharField(max_length=20, blank=True)
    trip_departure_time = models.CharField(max_length=20, blank=True)
    # will be populated from the route
    trip_fare = models.CharField(max_length=20, blank=True)
    status = models.CharField(choices=TRIP_STATUS_CHOICES, default="pending")
    bus_detail = models.ForeignKey(
        BusDetail, on_delete=models.SET_NULL, null=True, blank=True)  # not sure about this (null, blank) yet
    # these will be populated programatically using the
    # weekdaysSchedule and its corresponding departure time
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'TRIP {self.route} | on {self.trip_departure_date} | at {self.trip_departure_time} = {self.trip_id} {self.id}'

    def save(self, *args, **kwargs):
        # generate trip date and time using weekdaysschedule

        if not self.trip_departure_date or self.trip_departure_time:
            ''
        if not self.trip_id:
            # Create your custom format here
            date_part = datetime.date.today().strftime("%Y%m%d%H%M%S%p%j")
            random_part = uuid.uuid4().hex[:5].upper()
            self.trip_id = f"TRIP-{date_part}-{random_part}"
        super().save(*args, **kwargs)





'no coverage for those days yet, please pick a closer date'



# class DriversRoster(models.Model):
#     driver = models.ForeignKey(
#         Driver, on_delete=models.SET_DEFAULT, default='Driver')
#     dates_available = models.ManyToManyField()
        # will be activated when algorithm is developed


class Booking(models.Model):
    # most of booking's fields will get populated by Trip
    # and Trip will be triggered by WeekDaysSchedule
    STATUS_CHOICES = (("pending", "pending"), ("confirmed",
                                               "confirmed"), ("failed", "failed"), ("completed", "completed"))

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=45, blank=True, null=True)
    middlename = models.CharField(max_length=45, blank=True, null=True)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    booking_id = models.CharField(
        max_length=20, unique=True, editable=False, blank=True)

    email = models.EmailField(null=True, blank=True)
    location_from = models.ForeignKey(Location, verbose_name='From',
                                      on_delete=models.SET_NULL, related_name='location_from', null=True, blank=True)
    destination_to = models.ForeignKey(Location, verbose_name="To",
                                       on_delete=models.SET_NULL, related_name='destination_to', null=True, blank=True)
    trip = models.ForeignKey(
        Trip, on_delete=models.SET_NULL, null=True, blank=True)

    # locations will be used to find a route

    booked_route = models.ForeignKey(
        Route, on_delete=models.SET_NULL, null=True, blank=True)

    departure_date = models.DateField(null=True, blank=True)
    departure_time = models.CharField(max_length=100, null=True, blank=True)

    num_of_pass = models.PositiveIntegerField(
        verbose_name="Number of passengers", default=1, null=True, blank=True)

    bus_detail = models.ForeignKey(
        BusDetail, on_delete=models.SET_NULL, null=True, blank=True)

    payment_due = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending', null=True, blank=True)

    book_modified = models.DateTimeField(auto_now_add=True)
    book_created_at = models.DateTimeField(auto_now=True)
    feedback_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.booking_id}: {self.email} || Departure: {self.departure_date} - {self.departure_time} || Destination: from {self.location_from} to {self.destination_to}"

    def extend_departure_time_due_to_delay(self):
        pass

    def get_departure_dates_choices(self):
        selected_date = datetime.datetime.now()
        selected_date_data = WeekDaysSchedule.objects.filter(
            start_or_only_date=selected_date).first()
        scheduled_times_per_day = dict()
        if selected_date_data:
            for depart_time in selected_date_data.daily_schedule.time.all():
                format_time = f'{depart_time.hour}:{depart_time.minute}{depart_time.meridian}'
                scheduled_times_per_day[format_time] = format_time
        return scheduled_times_per_day

    def save(self, *args, **kwargs):
        if not self.booking_id:
            # Create your custom format here
            date_part = datetime.date.today().strftime("%Y%m%d")
            random_part = uuid.uuid4().hex[:5].upper()
            self.booking_id = f"BOOK-{date_part}-{random_part}"
        # if hasattr(self, 'payment'):
        # if self.status == 'pending':
        #     self.payment.status = 'pending'
        # if self.status == 'confirmed':
        #     self.payment.status = 'success'
        # if self.status == 'failed':
        #     self.payment.status = 'failed'

        super().save(*args, **kwargs)



class PaymentMethod(models.Model):
    title = models.CharField(max_length=45, null=True, blank=True)
    name = models.CharField(max_length=45)
    is_default = models.BooleanField(default=False)
    reference = models.CharField(max_length=85, null=True, blank=True)

    def __str__(self):
        return f'{self.title} {self.id}'


class Payment(models.Model):

    STATUS_CHOICES = (("pending", "pending"), ("success",
                      "success"), ("failed", "failed"), )

    booking = models.OneToOneField(Booking, related_name='payment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=3)
    payment_deadline = models.DateTimeField()
    method = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    reference = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][1])
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{ self.reference } For {self.booking.booking_id} | {self.booking.booked_route.__str__()}"
        # return self.booking.__str__()

    def save(self, *args, **kwargs):
        # print()
        # print("self.booking in save()", self.booking)
        # print()

        if not self.reference:
            today = timezone.now().strftime('%Y%m%d')
            rand = uuid.uuid4().hex[:5].upper()
            self.reference = f"PAY-{today}-{rand}"

        
        # if self.status == 'success':
        #     self.booking.status = 'confirmed'
        # if self.status == 'pending':
        #     self.booking.status = 'pending'
        # if self.status == 'failed':
        #     self.booking.status = 'failed'
        
        super().save(*args, **kwargs)



# print()
# print()
# print("self.daily_schedule", [f'{i.hour}:{i.minute}{i.meridian}'for i in self.daily_schedule.time.all()],  # values_list('hour', flat=True),
#     type(self.daily_schedule))
# print()
# print()
