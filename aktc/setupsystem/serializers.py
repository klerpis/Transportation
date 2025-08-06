from rest_framework import serializers
from .models import Location, DepartureTime

class LocationSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Location
        fields = ['state', 'local_government', 'bus_stop',
                  'street', 'lat', 'lng', 'image', ]

    def get_image(self, obj):
        request = self.context.get('request')
        if request and obj.image: 
            return request.build_absolute_uri(obj.image.url)
        return None 

class DepartureTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartureTime
        fields = ['id', 'time']

