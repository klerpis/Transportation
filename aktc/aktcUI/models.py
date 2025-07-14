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


class Location(models.Model):
    state = models.CharField(max_length=20)
    local_government = models.CharField(max_length=45)
    bus_stop = models.CharField(max_length=30)
    street = models.CharField(max_length=30, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'State: {self.state} || LG: {self.local_government}'


class Route(models.Model):
    from_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='from_location')
    to_destination = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='to_destination')
    fare = models.PositiveIntegerField(default=2000)
    journey_average_length = models.DurationField(default=timedelta(hours=1))
    add_reverse = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.from_location.state} → {self.to_destination.state}'

    def save(self, *args, **kwargs):

        if self.add_reverse and not self.id:
            if Route.objects.filter(from_location=self.to_destination,
                                    to_destination=self.from_location).first():
                raise exceptions.ValidationError(
                    _("This Route (location -> destination) already exists"))
            Route.objects.create(
                from_location=self.to_destination,
                to_destination=self.from_location,
                fare=self.fare,
                journey_average_length=self.journey_average_length,
                add_reverse=False,
            )
        return super().save(*args, **kwargs)


class Driver(models.Model):
    driver_name = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Driver's Name", on_delete=models.CASCADE)
    driver_phonenumber = models.CharField(
        "Driver's Phone Number", max_length=18, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    passport = models.ImageField(null=True, blank=True)  # not compulsory yet
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
    bus = models.ForeignKey(Bus, on_delete=models.DO_NOTHING)
    bus_driver = models.ForeignKey(Driver, on_delete=models.DO_NOTHING,
                                   blank=True, null=True)

    def __str__(self):
        self.return_ = f'''
            {self.bus.bus_name} || {self.bus.registration_number} || {self.bus.bus_status} || 
            '''
        return self.return_


class Trip(models.Model):

    TRIP_STATUS_CHOICES = [("pending", "Pending"), ("started", "Started"),
                           ("completed", "Completed"), ("cancelled", "Cancelled")]

    # leave blank
    trip_id = models.CharField(
        max_length=20, unique=True, editable=False, blank=True)

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
            date_part = datetime.date.today().strftime("%Y%m%d")
            random_part = uuid.uuid4().hex[:5].upper()
            self.trip_id = f"TRIP-{date_part}-{random_part}"
        super().save(*args, **kwargs)


class DepartureTime(models.Model):
    MERIDIAN_CHOICE = {
        "AM": 'am',
        "PM": 'pm'
    }
    HOUR_RANGE_CHOICE = {f"0{i}": f"0{i}" for i in range(0, 10)}
    HOUR_RANGE_CHOICE.update({f"{i}": f"{i}" for i in range(10, 13)})
    MINUTE_RANGE_CHOICE = {
        f"0{i}": f"0{i}" for i in range(0, 10) if i % 5 == 0}
    MINUTE_RANGE_CHOICE.update(
        {f"{i}": f"{i}" for i in range(10, 60) if i % 5 == 0})

    hour = models.CharField(choices=HOUR_RANGE_CHOICE,
                            default=list(HOUR_RANGE_CHOICE.keys())[0])
    minute = models.CharField(
        choices=MINUTE_RANGE_CHOICE, default=list(MINUTE_RANGE_CHOICE.keys())[0])
    meridian = models.CharField(
        choices=MERIDIAN_CHOICE, default=MERIDIAN_CHOICE["AM"])

    def __str__(self):
        return f"{self.hour}:{self.minute}{self.meridian}"

    # def __repr__(self):
    #     return super().__repr__()


class DailyScheduleTime(models.Model):
    time = models.ManyToManyField(
        DepartureTime, related_name='daily_schedule_time')

    def __str__(self):
        return f'{" || ".join([f"{i.hour}.{i.minute}{i.meridian}" for i in self.time.all()])}'


'no coverage for those days yet, please pick a closer date'


class PreviousSchedule(models.Model):
    start_or_only_date = models.DateField(
        verbose_name="Start/Only date", unique=True)
    # end_date = models.DateField(blank=True, null=True, unique=True)
    daily_schedule = models.ForeignKey(
        DailyScheduleTime, on_delete=models.DO_NOTHING, default='8')


def generate_id():
    code = int(str(int(uuid.uuid4()))[:random.randint(1, 9)])
    # gen_id = f"{previous_day_date}-{code}"
    return code


class WeekDaysSchedule(models.Model):
    # create Trips that match the departure dates and times

    def validate_start_date(start_date):  # cant be in the past
        cant_schedule_into_the_past = start_date > datetime.date.today() - \
            datetime.timedelta(hours=24, minutes=59, seconds=59)
        if (not cant_schedule_into_the_past):
            raise exceptions.ValidationError("Cannot schedule for past days")

    start_or_only_date = models.DateField(
        verbose_name="Start/Only date", unique=True, validators=[validate_start_date,])
    end_date = models.DateField(blank=True, null=True, unique=True)
    daily_schedule = models.ForeignKey(
        DailyScheduleTime, on_delete=models.DO_NOTHING, default='8')

    # create_trips_to_match_schedule = models.BooleanField(default=False)
    trip_route = models.ManyToManyField(Route, related_name='trip_route')
    # create a weekly schedule for a specific trip route (Lagos -> Abuja)

    def __str__(self):
        week: dict[int, str] = {
            0: 'Mon', 1: 'Tue', 2: 'Wed',
            3: 'Thur',
            4: 'Fri', 5: 'Sat', 6: 'Sun',
        }
        week_index = datetime.datetime.weekday(self.start_or_only_date)

        return f'Day: {str(week[week_index]).center(10, " ")} || Dates: {self.start_or_only_date} || Departure Times: {self.daily_schedule}'

    def clean(self):  # for end date validation
        if self.end_date is not None:
            if not (self.start_or_only_date < self.end_date):
                raise exceptions.ValidationError({
                    'end_date': _("End date cannot be before start date")})

        if self.end_date:
            # num of days inbetween
            days = abs((self.start_or_only_date - self.end_date).days)
            self.previous_date_list = []
            for day_count in range(days+1):
                previous_day_date = self.end_date - \
                    datetime.timedelta(days=day_count)
                if self.start_or_only_date == previous_day_date:
                    continue  # no need to add again
                default = WeekDaysSchedule.objects.filter(
                    start_or_only_date=previous_day_date)
                if len(default) > 0:
                    raise exceptions.ValidationError(
                        _("Dates in-between start and end date already exist in the database"))

                    # continue  # if date already exsit in database. then ignore
                # if self.end_date == previous_day_date: continue
                self.previous_date_list.append(previous_day_date)

        return super().clean()

    def save(self, *args, **kwargs):

        if hasattr(self, 'id') and (not self.id):
            self.id = generate_id()
            print()
            print('generate new id', self.id, self.trip_route.all(),
                  self.daily_schedule, self.start_or_only_date, self.end_date)
            print()
        else:
            print()
            print('old id is suffucient', self.id, self.trip_route.all())
            print()

        # old_schedules = WeekDaysSchedule.objects.filter(
        #     start_or_only_date__lt=datetime.datetime.now().date()-datetime.timedelta(days=1))
        # if old_schedules.first():
        #     for sch in old_schedules.all():
        #         PreviousSchedule.objects.create(
        #             start_or_only_date=sch.start_or_only_date,
        #             daily_schedule=sch.daily_schedule,
        #         )
        #         # not sure of syntax for delete
        #         WeekDaysSchedule.objects.delete(sch)

        super().save(*args, **kwargs)

        # print()
        # print('TRIP ROUTE CHECK', self.id, self.trip_route.all(),)
        # print()


# @receiver(m2m_changed, sender=Book.authors.through)
# def after_m2m_saved(sender, instance, action, **kwargs):
#     if action == "post_add" or action == "post_remove":
#         authors = instance.authors.all()  # ✅ M2M data is ready
#         print(f"Updated authors for {instance.title}: {authors}")
#         # Run your logic here


@receiver(m2m_changed, sender=WeekDaysSchedule.trip_route.through)
def post_save_create_trips(sender, instance, action, **kwargs):
    if action == "post_add" or action == "post_remove":
        print("beginning created Id", instance.id, instance.trip_route.all(),
              instance.start_or_only_date)
        # all_weekdays = []
        if instance.end_date:
            print("trip to be created Id", instance.id)
            date_list = [i for i in instance.previous_date_list]
            for previous_day_date in date_list:
                new_data = WeekDaysSchedule(
                    start_or_only_date=previous_day_date,
                    daily_schedule=instance.daily_schedule,
                    # trip_route=instance.trip_route,
                )
                new_data.id = generate_id()
                # new_data.trip_route.set([])
                new_data.trip_route.set(instance.trip_route.all())
                # instance.previous_date_list.remove(previous_day_date)
                # all_weekdays.append(new_data)
                new_data.save()
            instance.end_date = None  # clear end date

        print("t_route created Id", instance.id, instance.trip_route.all(),
              instance.start_or_only_date)
        # all_trips = []
        for t_route in instance.trip_route.all():
            for period in instance.daily_schedule.time.all():
                print("period created Id", instance.id, period,
                      instance.daily_schedule.time.all())
                if Trip.objects.filter(
                    trip_departure_date=instance.start_or_only_date,
                    trip_departure_time=period, route=t_route
                ).first():
                    print("trip already exists", instance.id)
                    continue
                else:
                    trip = Trip(
                        route=t_route,
                        trip_departure_date=instance.start_or_only_date,
                        trip_departure_time=period,
                        status='pending',
                        trip_fare=t_route.fare,
                        # trip_id='', # will be generated in trip save
                        # seats_booked='', # defaults to zero
                        # bus_detail='', #

                    )

                    # all_trips.append(trip)
                    trip.save()

        # WeekDaysSchedule.objects.bulk_create(all_weekdays)
        # Trip.objects.bulk_create(all_trips)

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
        super().save(*args, **kwargs)


class Feedback(models.Model):

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    rating = models.PositiveIntegerField()  # e.g. 1–5 stars
    submitted_at = models.DateTimeField(auto_now_add=True)
    trip_books = models.ForeignKey(Booking, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-submitted_at']

    def is_valid_window(self):
        return timezone.now() <= self.booking.departure_date + timedelta(hours=48)

    def __str__(self):
        return f"Feedback for {self.trip_books.booking_id}"


class Review(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    published = models.BooleanField(default=False)  # admin approves
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name}"


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

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
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
        if self.status == 'success':
            self.booking.status = 'completed'
        super().save(*args, **kwargs)


class SupportTicket(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} ({'✓' if self.resolved else '✗'})"


# print()
# print()
# print("self.daily_schedule", [f'{i.hour}:{i.minute}{i.meridian}'for i in self.daily_schedule.time.all()],  # values_list('hour', flat=True),
#     type(self.daily_schedule))
# print()
# print()
