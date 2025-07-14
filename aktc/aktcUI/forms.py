from django import forms
from datetime import date
from . import models

# forms.


class BookTicketForm(forms.ModelForm):
    ''
    class Meta:
        model = models.Booking
        fields = "__all__"
        widgets = {
            'departure_date': forms.TextInput(attrs={"data-flatpickr": 'true',
                                                     'class': 'vTextField', 'placeholder': 'Pick a date for departure'}),
            'firstname': forms.TextInput(attrs={'class': 'vTextField', 'id': 'booking-first-name', 'placeholder': 'first name'}),
            'middlename': forms.TextInput(attrs={'class': 'vTextField', 'id': 'booking-midddle-name', 'placeholder': 'Middle name'}),
            'surname': forms.TextInput(attrs={'class': 'vTextField', 'id': 'booking-surname', 'placeholder': 'Surname'}),
            'email': forms.EmailInput(attrs={'class': 'vTextField', 'id': 'booking-email', 'placeholder': 'input a valid email'}),
            'departure_time': forms.Select(attrs={'class': 'vTextField',
                                                  'id': 'booking-departure-time', 'placeholder': 'Choose your departure time'}),
            # 'location_from': forms.Select(attrs={'class': 'vTextField', 'id': 'booking-location-from'}),
            # 'destination_to': forms.Select(attrs={'class': 'vTextField', 'id': 'booking-destination-to'}),
            # 'bus_detail': forms.Select(attrs={'class': 'vTextField', 'id': 'booking-bus-details'}),
            # 'date_modified': forms.TextInput(attrs={'class': 'vTextField', 'id': 'booking-date-modified'}),
            # 'date_created': forms.TextInput(attrs={'class': 'vTextField', 'id': 'booking-date-created'}),

        }

    class Media:
        css = {
            'all': ('aktcUI/css/flatpickr.min.css',)
        }
        js = (
            'aktcUI/js/flatpickr.min.js',
            'aktcUI/js/admin_flatpickr.js')
