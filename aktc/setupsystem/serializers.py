from rest_framework import serializers
from .models import Location, DepartureTime

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['state', 'local_government', 'bus_stop',
                  'street', 'lat', 'lng']


class DepartureTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartureTime
        fields = ['id', 'time']

