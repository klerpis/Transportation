# import datetime
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from django.contrib.admin import AdminSite, ModelAdmin
from django.shortcuts import render
from django.urls import path
from django.template.response import TemplateResponse

import uuid
import random

from accounts.models import Profile
from aktcUI import forms
from aktcUI import models
# from


class BoardAktcAdminSite(AdminSite):
    site_header = 'AKTC Board Room'
    site_title = 'Greetings, Board Room'
    index_title = 'Welcome to the Board Room'


class AktcAdminSite(AdminSite):
    site_header = 'AKTC Administration'
    site_title = 'Greetings, Administration'
    index_title = 'Welcome to the Admin Dashboard'

    def confirm_passenger_arrival(self, request):
        request.current_app = self.name
        context = dict(
            self.each_context(request),
        )
        return TemplateResponse(request, 'admin/confirm_passenger.html', context)
    # return render(request, 'admin/confirm_passenger.html', {})

    def get_urls(self):
        urls = super().get_urls()
        aktc_new_urls = [path("confirmpass/", self.admin_view(
            self.confirm_passenger_arrival), name='confirmpass')]

        return aktc_new_urls + urls


# aktc_admin_site.register(models.Bus)


class BookTicketAdmin(ModelAdmin):
    form = forms.BookTicketForm


def generate_id():
    code = int(str(int(uuid.uuid4()))[:random.randint(1, 9)])
    # gen_id = f"{previous_day_date}-{code}"
    return code


class WeekDaysScheduleAdmin(ModelAdmin):
    pass
    # def save_related(self, request, form, formsets, change):
    #     super().save_related(request, form, formsets, change)
    #     instance = form.instance

    #     if instance.end_date:
    #         print("trip to be created Id", instance.id)
    #         date_list = [i for i in instance.previous_date_list]
    #         for previous_day_date in date_list:
    #             new_data = models.WeekDaysSchedule(
    #                 start_or_only_date=previous_day_date,
    #                 daily_schedule=instance.daily_schedule,
    #                 # trip_route=instance.trip_route,
    #             )
    #             new_data.id = generate_id()
    #             new_data.trip_route.set(instance.trip_route.all())
    #             # instance.previous_date_list.remove(previous_day_date)
    #             new_data.save()
    #         instance.end_date = None  # clear end date

    #     print("Admin t_route created Id", instance.trip_route.all())
    #     for t_route in instance.trip_route.all():
    #         print("Admin t_route loop", t_route)
    #         for period in instance.daily_schedule.time.all():
    #             print("Admin period ", period,
    #                   instance.daily_schedule.time.all())
    #             if models.Trip.objects.filter(
    #                 trip_departure_date=instance.start_or_only_date,
    #                 trip_departure_time=period, route=t_route
    #             ).first():
    #                 print("=========================")
    #                 print("admin trip already exists")
    #                 print("=========================")
    #                 continue
    #             else:
    #                 trip = models.Trip(
    #                     route=t_route,
    #                     trip_departure_date=instance.start_or_only_date,
    #                     trip_departure_time=period,
    #                     status='pending',
    #                     trip_fare=t_route.fare,
    #                     # trip_id='', # will be generated in trip save
    #                     # seats_booked='', # defaults to zero
    #                     # bus_detail='', #
    #                 )
    #                 trip.save()


aktc_admin_site = AktcAdminSite(name='aktc_admin')
board_room = BoardAktcAdminSite(name='board_room')


add_models = [models.Bus, models.Customer,
              models.BusDetail, models.Driver, models.Location,
              models.DepartureTime, models.DailyScheduleTime,
              models.Feedback, models.PaymentMethod, models.Payment,
              Profile, models.Trip, models.PreviousSchedule,
              models.Review, models.SupportTicket, models.Route,
              ]

# UserAdmin, GroupAdmin
aktc_admin_site.register([*add_models])

aktc_admin_site.register(models.Booking, BookTicketAdmin)
aktc_admin_site.register(models.WeekDaysSchedule, WeekDaysScheduleAdmin)

board_room.register([*add_models])

board_room.register(models.Booking, BookTicketAdmin)
board_room.register(models.WeekDaysSchedule, WeekDaysScheduleAdmin)

board_room.register(Group, GroupAdmin)
board_room.register(User, UserAdmin)
    