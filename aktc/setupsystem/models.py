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


class Location(models.Model):
    state = models.CharField(max_length=20)
    local_government = models.CharField(max_length=45)
    bus_stop = models.CharField(max_length=30)
    street = models.CharField(max_length=30, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='location/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f'LG: {self.local_government} ({self.state})'


class Route(models.Model):
    from_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='from_location')
    to_destination = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='to_destination')
    fare = models.PositiveIntegerField(default=2000)
    journey_average_length = models.DurationField(default=timedelta(hours=1))
    add_reverse = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.from_location.state} ({self.from_location.local_government}) → {self.to_destination.state} ({self.to_destination.local_government})'

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

    class Meta:
        verbose_name = 'Departure Time (hour of day)'
        verbose_name_plural = 'Departure Time (hour of day)'

    # def __repr__(self):
    #     return super().__repr__()


class DailyScheduleTime(models.Model):
    time = models.ManyToManyField(
        DepartureTime, related_name='daily_schedule_time')

    class Meta:
        verbose_name = 'Daily Schedule (Time)'
        verbose_name_plural = 'Daily Schedule (Multiple Departure Times per day)'

    def __str__(self):
        return f'{" || ".join([f"{i.hour}.{i.minute}{i.meridian}" for i in self.time.all()])}'


class PreviousSchedule(models.Model):
    start_or_only_date = models.DateField(
        verbose_name="Start/Only date", unique=True)
    # end_date = models.DateField(blank=True, null=True, unique=True)
    daily_schedule = models.ForeignKey(
        DailyScheduleTime, on_delete=models.DO_NOTHING, default='8')


def generate_int_id():
    code = int(uuid.uuid4())
    # gen_id = f"{previous_day_date}-{code}"
    return code


def generate_id():
    code = int(str(int(uuid.uuid4()))[:random.randint(1, 9)])
    # gen_id = f"{previous_day_date}-{code}"
    return code


class WeekDaysSchedule(models.Model):
    # create Trips that match the departure dates and times

    class Meta:
        verbose_name = 'Week day Schedule'
        verbose_name_plural = 'Week day Schedule'

    def validate_start_date(start_date):  # cant be in the past
        cant_schedule_into_the_past = start_date > datetime.date.today() - \
            datetime.timedelta(hours=24, minutes=59, seconds=59)
        if (not cant_schedule_into_the_past):
            raise exceptions.ValidationError("Cannot schedule for past days")

    start_or_only_date = models.DateField(
        verbose_name="Start/Only date", validators=[validate_start_date,])
    end_date = models.DateField(blank=True, null=True)
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

    previous_date_list = set()

    def clean(self):  # for end date validation

        if self.end_date is not None:
            if not (self.start_or_only_date < self.end_date):
                raise exceptions.ValidationError({
                    'end_date': _("End date cannot be before start date")})

        if self.end_date:
            # num of days inbetween
            days = abs((self.start_or_only_date - self.end_date).days)
            print("1")
            for day_count in range(days+1):
                previous_day_date = self.end_date - \
                    datetime.timedelta(days=day_count)
                print("2")
                # if self.start_or_only_date == previous_day_date:
                #     continue  # no need to add again
                print("3")

                # default = WeekDaysSchedule.objects.filter(
                #     start_or_only_date=previous_day_date,
                #     )
                # if len(default) > 0:
                #     print("5 Error")

                #     raise exceptions.ValidationError(
                #         _("Dates in-between start and end date already exist in the database"))
                # continue  # if date already exsit in database. then ignore
                # if self.end_date == previous_day_date: continue
                self.previous_date_list.add(previous_day_date)
        # else:

        #     default_exists = WeekDaysSchedule.objects.filter(
        #         start_or_only_date=self.start_or_only_date,
        #         ).first()
        #     if default_exists:
        #         raise exceptions.ValidationError(
        #             _("Dates in-between start and end date already exist in the database"))

        return super().clean()

    initial_week_day_check = False

    def save(self, *args, **kwargs):

        if hasattr(self, 'id') and (not self.id):
            self.initial_week_day_check = True
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
