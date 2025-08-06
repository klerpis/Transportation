# import datetime
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.template.response import TemplateResponse

import uuid
import random

from accounts.models import Profile
from aktcUI import forms
from aktcUI import models
from feedbacksystem import models as feedbackmodels

from setupsystem import models as setupsystemmodels

class ExtraPageSite:
    admin_type = 'admin'

    # def index(self, request, extra_context = None):
    #     return redirect(f'/{self.admin_type}/help/')

    def confirm_passenger_arrival(self, request):
        request.current_app = self.name
        context = dict(
            self.each_context(request),
        )
        return TemplateResponse(request, 'admin/confirm_passenger.html', context)

    def helpview(self, request):
        request.current_app = self.name
        context =  dict(
            self.each_context(request),
        )
        return TemplateResponse(request, 'admin/help.html', context)

    # return render(request, 'admin/confirm_passenger.html', {})

    def get_urls(self):
        urls = super().get_urls()
        aktc_new_urls = [
            path("confirmpass/", self.admin_view(
            self.confirm_passenger_arrival), name='confirmpass'),
            path("help/", self.admin_view(
            self.helpview), name='helpview'),]
        # print("aktc_new_urls", urls)
        return aktc_new_urls + urls

class BoardAktcAdminSite(ExtraPageSite, AdminSite):
    site_header = 'AKTC Board Room'
    site_title = 'Greetings, Board Room'
    index_title = 'Welcome to the Board Room'
    admin_type = 'board'

class AktcAdminSite(ExtraPageSite, AdminSite):
    site_header = 'AKTC Administration'
    site_title = 'Greetings, Administration'
    index_title = 'Welcome to the Admin Dashboard'
    admin_type = 'admin'



# aktc_admin_site.register(models.Bus)

class PaymentInline(admin.TabularInline):
    model = models.Payment
    extra = 0


class BookTicketAdmin(ModelAdmin):
    form = forms.BookTicketForm
    inlines = [PaymentInline,]
    
    list_display = ['id', 'customer_name', 'booking_id', 'trip_id', 'status' ]
    list_display_links = ['customer_name', 'booking_id']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['booking_id', 'customer_name', 'trip_id', 'payment_id']
    readonly_fields = ['booking_id']

    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def trip_id(self, obj):
        return obj.trip.trip_id
    
    def payment_id(self, obj):
        return obj.payment.reference

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # List fields that should be read-only when editing
            return ('customer', 'booked_route', 
                    'booking_id',) 
        else:  # Creating a new object
            # Return an empty tuple or a list of fields that are always read-only
            return () # All fields are writable during creation


def generate_id():
    code = int(str(int(uuid.uuid4()))[:random.randint(1, 9)])
    # gen_id = f"{previous_day_date}-{code}"
    return code


class WeekDaysScheduleAdmin(ModelAdmin):
    pass


aktc_admin_site = AktcAdminSite(name='aktc_admin')
board_room = BoardAktcAdminSite(name='board_room')


# @board_room.register(models.Bus)
class BusAdmin(ModelAdmin):
    list_display = ['registration_number', 'bus_name', 'bus_seat_num', 'bus_status' ]
    list_filter = ['bus_status']
    list_editable = ['bus_status', 'bus_seat_num']
    search_fields = ['registration_number', 'bus_name']
    # readonly_fields = ['registration_number']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # List fields that should be read-only when editing
            return ('registration_number', ) 
        else:  # Creating a new object
            # Return an empty tuple or a list of fields that are always read-only
            return () # All fields are writable during creation


aktc_admin_site.register(models.Bus, BusAdmin)
board_room.register(models.Bus, BusAdmin)

class CustomerAdmin(ModelAdmin):
    list_display = ['user__username', 'phone_number', 'email']
    # list_filter = []
    # list_editable = []
    search_fields = ['email', 'user__username', 'firstname', 'surname']
    readonly_fields = ['user']

    fieldsets = (
        ('Credentials', {"fields": ['user', 'firstname', 'middlename', 'surname', 'email']}),
        ('Extra data', {'fields': ['phone_number']}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # List fields that should be read-only when editing
            return ('user',) 
        else:  # Creating a new object
            # Return an empty tuple or a list of fields that are always read-only
            return () # All fields are writable during creation


aktc_admin_site.register(models.Customer, CustomerAdmin)
board_room.register(models.Customer, CustomerAdmin)


class LocationAdmin(ModelAdmin):
    list_display = ['state', 'local_government', 'bus_stop', 'street', 'lat', 'lng', 'featured']
    list_editable = ['lat', 'lng', 'featured',]
    search_fields = ['state', 'local_government', 'bus_stop', 'street', 'lat', 'lng']
    # readonly_fields = []

    fieldsets = (
        ('Address', {"fields":  ['state', 'local_government', 'bus_stop', 'street']}),
        ('Geographic Coordinates', {'fields': [ 'lat', 'lng']}),
        ("Display", {'fields': [ 'featured', 'image', 'description']}),
        
    )
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # List fields that should be read-only when editing
            return ('state', 'local_government',) 
        else:  # Creating a new object
            # Return an empty tuple or a list of fields that are always read-only
            return () # All fields are writable during creation

aktc_admin_site.register(setupsystemmodels.Location, LocationAdmin)
board_room.register(setupsystemmodels.Location, LocationAdmin)

class DepartureTimeAdmin(ModelAdmin):
    list_display = ['hour', 'minute', 'meridian']
    list_filter = ['meridian']

aktc_admin_site.register(setupsystemmodels.DepartureTime, DepartureTimeAdmin)
board_room.register(setupsystemmodels.DepartureTime, DepartureTimeAdmin)


@admin.action(description="Update selected items' status to completed")
def update_status_to_published(modeladmin, request, queryset):
    queryset.update(status='completed')
    modeladmin.message_user(request, f"{queryset.count()} items were successfully updated to 'completed'.")
    

class TripAdmin(ModelAdmin):
    list_display = ['trip_id', 'route', 
    'seats_booked', 'trip_departure_date', 'trip_departure_time', 
    'trip_fare', 'status']
    list_filter = ['trip_departure_date', 'trip_departure_time', 'status']
    list_editable = ['status']
    # readonly_fields = ['trip_id', 'route', 'seats_booked', 'trip_departure_date', 'trip_departure_time', 
    # 'trip_fare']
    actions = [update_status_to_published]
    search_fields = ['seats_booked', 'route__from_location__state', 
                    'route__to_destination__state',  ]
    fieldsets = (
        ('Trip Data', {"fields":  ['route', 'trip_departure_date', # 'trip_id',  
        'trip_departure_time', 'trip_fare']}),
        ('Dynamic Info', {'fields': [ 'seats_booked', 'status']}),
    )
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # List fields that should be read-only when editing
            return ('trip_id', 'route', 
                    'seats_booked', 'trip_departure_date',) 
        else:  # Creating a new object
            # Return an empty tuple or a list of fields that are always read-only
            return () # All fields are writable during creation


aktc_admin_site.register(models.Trip, TripAdmin)
board_room.register(models.Trip, TripAdmin)



class FeedbackAdmin(ModelAdmin):
    list_display = ['user', 'rating', 'booking_id', 
        #'trip_id'
    ]
    list_filter = ['rating']
    # list_editable = []
    # readonly_fields = ['user', 'comment', 'rating', 'submitted_at', 'trip_books']
    search_fields = ['trip_books__booking_id', 'trip_books__trip__trip_id',
    'trip_books__location_from__state', 'trip_books__destination_to__state']
    fieldsets = (
        ('Passenger Data', {"fields":  ['user', 'comment', 'rating', 
        'submitted_at']}),
        ('Trip Data', {'fields': [ 'trip_books']}),
    )
    # inlines = [RouteInline,]
    
    def booking_id(self, obj):
        return obj.trip_books.booking_id

    def trip_id(self, obj):
        return obj.trip_books.trips.trip_id
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # List fields that should be read-only when editing
            return ('user', 'comment', 
                    'rating', 'submitted_at', 'trip_books',) 
        else:  # Creating a new object
            # Return an empty tuple or a list of fields that are always read-only
            return () # All fields are writable during creation



aktc_admin_site.register(feedbackmodels.Feedback, FeedbackAdmin)
board_room.register(feedbackmodels.Feedback, FeedbackAdmin)


class TripInline(admin.TabularInline):
    model = models.Trip
    extra = 0

class RouteAdmin(ModelAdmin):
    list_display = ['from_location', 'to_destination', 
                'fare', 'journey_average_length']
    # list_filter = []
    list_editable = ['fare', 'journey_average_length']
    # readonly_fields = ['from_location', 'to_destination']
    search_fields = ['from_location__state', 'to_destination__state',
    'from_location__local_government', 'to_destination__local_government',
    'from_location__bus_stop', 'to_destination__bus_stop',
    'from_location__street', 'to_destination__street',
    ]
    # fieldsets = (
    #     ('Passenger Data', {"fields":  ['user', 'comment', 'rating', 
    #     'submitted_at']}),
    #     ('Trip Data', {'fields': [ 'trip_books', 'submitted_at']}),
    # )
    inlines = [TripInline,]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # List fields that should be read-only when editing
            return ('from_location', 'to_destination',) 
        else:  # Creating a new object
            # Return an empty tuple or a list of fields that are always read-only
            return () # All fields are writable during creation



aktc_admin_site.register(setupsystemmodels.Route, RouteAdmin)
board_room.register(setupsystemmodels.Route, RouteAdmin)

# class DepartureTimeInline(admin.TabularInline):
#     model = models.DepartureTime
#     extra = 0

# class DailyScheduleTimeAdmin(ModelAdmin):
#     # list_display = ['time']
#     # list_filter = []
#     # list_editable = []
#     # readonly_fields = []
#     # search_fields = []
#     # fieldsets = (
#     #     ('Passenger Data', {"fields":  ['user', 'comment', 'rating', 
#     #     'submitted_at']}),
#     #     ('Trip Data', {'fields': [ 'trip_books', 'submitted_at']}),
#     # )
#     inlines = [DepartureTimeInline,]

#     # def display_time(self, obj):
#     #     return obj

# aktc_admin_site.register(models.DailyScheduleTime, DailyScheduleTimeAdmin)
# board_room.register(models.DailyScheduleTime, DailyScheduleTimeAdmin)


class ReviewAdmin(ModelAdmin):
    list_display = ['name', 'email', 
                'rating', 'published']
    list_filter = ['published', 'rating']
    list_editable = ['published']
    # readonly_fields = ['name', 'email', 'rating']
    search_fields = ['name', 'email']
    # fieldsets = (
    #     ('Passenger Data', {"fields":  ['user', 'comment', 'rating', 
    #     'submitted_at']}),
    #     ('Trip Data', {'fields': [ 'trip_books', 'submitted_at']}),
    # )
    # inlines = [ReviewInline,]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # List fields that should be read-only when editing
            return ('name', 'email', 'rating',) 
        else:  # Creating a new object
            # Return an empty tuple or a list of fields that are always read-only
            return () # All fields are writable during creation


aktc_admin_site.register(feedbackmodels.Review, ReviewAdmin)
board_room.register(feedbackmodels.Review, ReviewAdmin)

    

class PaymentAdmin(ModelAdmin):
    list_display = ['reference', 'amount', 
                'booking_id', 'method', 'status']
    list_filter = ['status', 'payment_deadline']
    list_editable = ['status']
    readonly_fields = ['created', 'reference', 'booking']
    search_fields = ['reference', 'amount']
    # fieldsets = (
    #     ('Passenger Data', {"fields":  ['user', 'comment', 'rating', 
    #     'submitted_at']}),
    #     ('Trip Data', {'fields': [ 'trip_books', 'submitted_at']}),
    # )

    def booking_id(self, obj):
        return obj.booking.booking_id
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # List fields that should be read-only when editing
            return ('created', 'reference', 
                    'booking', ('status' if obj.status!='pending' else '' )) 
        else:  # Creating a new object
            # Return an empty tuple or a list of fields that are always read-only
            return () # All fields are writable during creation


aktc_admin_site.register(models.Payment, PaymentAdmin)
board_room.register(models.Payment, PaymentAdmin)

class PaymentMethodAdmin(ModelAdmin):
    list_display = ['title', 'name']
    # list_filter = ['status', 'PaymentMethod_deadline']
    list_editable = []
    # readonly_fields = []
    # search_fields = ['reference', 'amount']
    # fieldsets = (
    #     ('Passenger Data', {"fields":  ['user', 'comment', 'rating', 
    #     'submitted_at']}),
    #     ('Trip Data', {'fields': [ 'trip_books', 'submitted_at']}),
    # )
    # inlines = [BookingInline,]

aktc_admin_site.register(models.PaymentMethod, PaymentMethodAdmin)
board_room.register(models.PaymentMethod, PaymentMethodAdmin)

class ProfileAdmin(ModelAdmin):

    list_display = ['user__username', 'email']
    # list_filter = ['status', 'PaymentMethod_deadline']
    # list_editable = ['status']
    readonly_fields = ['user', ]
    search_fields = ['user__username', 'email', 'phonenumber']
    # fieldsets = (
    #     ('Passenger Data', {"fields":  ['user', 'comment', 'rating', 
    #     'submitted_at']}),
    #     ('Trip Data', {'fields': [ 'trip_books', 'submitted_at']}),
    # )
    # inlines = [BookingInline,]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # List fields that should be read-only when editing
            return ('user',) 
        else:  # Creating a new object
            # Return an empty tuple or a list of fields that are always read-only
            return () # All fields are writable during creation


aktc_admin_site.register(Profile, ProfileAdmin)
board_room.register(Profile, ProfileAdmin)


add_models = [setupsystemmodels.DailyScheduleTime,
              models.BusDetail, models.Driver,
              setupsystemmodels.PreviousSchedule, 
              feedbackmodels.SupportTicket,
              ]

# UserAdmin, GroupAdmin
aktc_admin_site.register([*add_models])

aktc_admin_site.register(models.Booking, BookTicketAdmin)
aktc_admin_site.register(setupsystemmodels.WeekDaysSchedule, WeekDaysScheduleAdmin)

board_room.register([*add_models])

board_room.register(models.Booking, BookTicketAdmin)
board_room.register(setupsystemmodels.WeekDaysSchedule, WeekDaysScheduleAdmin)

board_room.register(Group, GroupAdmin)
board_room.register(User, UserAdmin)
