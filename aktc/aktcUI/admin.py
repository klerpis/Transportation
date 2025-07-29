from django.urls import path
import datetime
from django.contrib import admin
from django import forms
from . import models
from . import forms
from django.template.response import TemplateResponse
# from django.contrib.admin.ModelAdmin import message_user

# admin.AdminSite()
# admin.DateFieldListFilter()
# admin.SimpleListFilter()


class Scheduler(admin.ModelAdmin):

    def confirm_passenger_arrival(self, request):
        request.current_app = self.admin_site.name
        context = dict(
            self.admin_site.each_context(request),
        )
        return TemplateResponse(request, 'admin/confirm_passenger.html', context)
    # return render(request, 'admin/confirm_passenger.html', {})

    def get_urls(self):

        urls = super().get_urls()
        aktc_new_urls = [path("confirmpass/", self.admin_site.admin_view(
            self.confirm_passenger_arrival), name='confirmpass')]

        return urls + aktc_new_urls

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'departure_time':
    #         kwargs['queryset'] = self.get_departure_dates_choices()
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_departure_dates_choices(self):
    #     selected_date = datetime.datetime.now()
    #     selected_date_data = models.WeekDaysSchedule.objects.filter(
    #         start_or_only_date=selected_date).first()
    #     scheduled_times_per_day = list()
    #     if selected_date_data:
    #         for depart_time in selected_date_data.daily_schedule.time.all():
    #             format_time = f'{depart_time.hour}:{depart_time.minute}{depart_time.meridian}'
    #             scheduled_times_per_day.append(format_time)
    #             # scheduled_times_per_day[format_time] = format_time
    #     return scheduled_times_per_day


# admin.site.register()
# admin.site = BoardAktcAdminSite(name='board_room')
# admin_site_path = [path('aktc_admin/', admin.site.urls)]
