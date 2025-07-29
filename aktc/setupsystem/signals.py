
from django.dispatch import receiver

from .models import WeekDaysSchedule
from aktcUI.models import Trip
import uuid
import random


from django.db.models.signals import m2m_changed
from django.dispatch import receiver


def generate_id():
    code = int(str(int(uuid.uuid4()))[:random.randint(1, 9)])
    # gen_id = f"{previous_day_date}-{code}"
    return code


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
