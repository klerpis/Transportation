
from django.dispatch import receiver

from .models import WeekDaysSchedule
from aktcUI.models import Trip
import uuid
import random


import datetime

from django.db.models.signals import m2m_changed
from django.dispatch import receiver


def generate_id():
    code = int(str(int(uuid.uuid4()))[:random.randint(1, 9)])
    # gen_id = f"{previous_day_date}-{code}"
    return code


# @receiver(post_save, sender=WeekDaysSchedule)
# def post_save_trigger_date_schedule_minimize_memory_usage(sender, instance, action, **kwargs):
#     if action == "created":
#         ''


def generate_trip_id():
    date_part = datetime.date.today().strftime("%Y%m%d%H%M%S%p%j")
    random_part = uuid.uuid4().hex[:5].upper()
    return f"TRIP-{date_part}-{random_part}"


# @receiver(m2m_changed, sender=WeekDaysSchedule.trip_route.through)
# def post_save_create_trips(sender, instance, action, **kwargs):
#     ''


@receiver(m2m_changed, sender=WeekDaysSchedule.trip_route.through)
def post_save_create_trips(sender, instance, action, **kwargs):
    print("whatuuuuuuuuuuuuuuuuuuuuuuuuuu")

    if action == "post_add":  # or action == "post_remove":
        print("beginning created Id", instance.id, instance.trip_route.all(),
              instance.start_or_only_date)
        all_weekdays = []
        date_list = set()
        all_trips = []
        print('its started')
        # instance_new_data = WeekDaysSchedule.objects.filter(
        #     start_or_only_date=instance.start_or_only_date,)

        # if not created:
        #     new_data.id = generate_id()
        #     new_data.initial_week_day_check = False
        #     # new_data.trip_route.set([])
        #     new_data.trip_route.clear()
        # new_data.daily_schedule=instance.daily_schedule,

        if instance.end_date:
            print('its started 2')
            print("trip to be created Id", instance.id)
            date_list = [i for i in instance.previous_date_list]
            print('its started datelist', date_list)

            for previous_day_date in date_list:
                try:
                    new_data_list = WeekDaysSchedule.objects.filter(
                        start_or_only_date=previous_day_date,)
                    if len(new_data_list) < 1:
                        new_data = WeekDaysSchedule(
                            start_or_only_date=previous_day_date,)
                        new_data.id = generate_id()
                    elif len(new_data_list) > 1:
                        new_data = new_data_list.filter(
                            daily_schedule=instance.daily_schedule,).first()
                        old_data = new_data_list.exclude(
                            daily_schedule=instance.daily_schedule,).first()
                        Trip.objects.filter(
                            trip_departure_date=previous_day_date).delete()
                        old_data.delete()

                        # raise Exception("Greater than 1 error", len(new_data_list), new_data_list)
                    else:
                        new_data = new_data_list[0]
                    new_data.initial_week_day_check = False
                    new_data.daily_schedule = instance.daily_schedule
                    new_data.trip_route.set(
                        instance.trip_route.all(), clear=False)

                    # instance.previous_date_list.remove(previous_day_date)
                    all_weekdays.append(new_data)
                    # new_data.save()
                except Exception as e:
                    print("EEEEEEE", e)
                    raise Exception(e)
            instance.end_date = None  # clear end date
            print('its started done with datelist')

        # print("t_route created Id", instance.id, instance.trip_route.all(),
        #       instance.start_or_only_date)
        # date_list = date_list or []
        print('its started 3')
        # initial_week_day_check = first instance used to generate the remaining
        # date trips inbetween and end date
        if instance.initial_week_day_check:
            for t_route in instance.trip_route.all():
                print("A single route", t_route, )
                for period in instance.daily_schedule.time.all():
                    for previous_day_date in date_list:
                        print("period created Id", instance.id, period,
                              instance.daily_schedule.time.all())
                        if Trip.objects.filter(
                            trip_departure_date=previous_day_date,
                            trip_departure_time=period, route=t_route
                        ).first():
                            print("trip already exists", instance.id)
                            continue
                        else:
                            trip = Trip(
                                trip_id=generate_trip_id(),
                                route=t_route,
                                trip_departure_date=previous_day_date,
                                trip_departure_time=period,
                                status='pending',
                                trip_fare=t_route.fare,
                                # trip_id='', # will be generated in trip save
                                # seats_booked='', # defaults to zero
                                # bus_detail='', #
                            )
                            all_trips.append(trip)

                    # for the original ---------
                    print('its started4')
                    if Trip.objects.filter(
                        trip_departure_date=instance.start_or_only_date,
                        trip_departure_time=period, route=t_route
                    ).first():
                        print("trip already exists", instance.id)
                        continue
                        # break # dont let multiple repeated departure set
                    else:
                        trip = Trip(
                            trip_id=generate_trip_id(),
                            route=t_route,
                            trip_departure_date=instance.start_or_only_date,
                            trip_departure_time=period,
                            status='pending',
                            trip_fare=t_route.fare,
                            # trip_id='', # will be generated in trip save
                            # seats_booked='', # defaults to zero
                            # bus_detail='', #
                        )
                        all_trips.append(trip)

                        # trip.save()

        # WeekDaysSchedule.objects.bulk_create(all_weekdays)
        print('its started5')
        try:
            if all_trips:
                Trip.objects.bulk_create(all_trips)
        except Exception as e:
            print("ERRRRRooo", e)
            raise Exception(e)
        print('its started6')
        multiple_instance = WeekDaysSchedule.objects.filter(
            start_or_only_date=instance.start_or_only_date)
        if len(multiple_instance) > 1:
            # current_instance = list(filter(
            #     lambda arg: arg is instance, multiple_instance))[0]
            first_instance = list(filter(
                lambda arg: arg is not instance, multiple_instance))[0]

            first_instance.daily_schedule = instance.daily_schedule
            # first_instance.trip_route.clear()
            first_instance.trip_route.set(
                instance.trip_route.all(), clear=False)

            instance.delete()
        else:
            instance.save()

        for weekdays in all_weekdays:
            weekdays.initial_week_day_check = False
            weekdays.save()

        print('its started7')
