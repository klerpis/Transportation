from django.shortcuts import render

from rest_framework import generics #, status
from .models import Location
from .serializers import LocationSerializer

class LocationListAPIView(generics.ListAPIView):
    serializer_class = LocationSerializer
    permission_classes = []  # You can make this IsAuthenticated later if needed
    queryset = Location.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def get_queryset(self):
        # email = self.request.query_params.get('email')
        # user = self.request.user if self.request.user.is_authenticated else None
        locs = Location.objects.all()
        print("locs", locs)
        return locs

class FeaturedLocationListAPIView(generics.ListAPIView):
    serializer_class = LocationSerializer
    permission_classes = []  # You can make this IsAuthenticated later if needed
    queryset = Location.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def get_queryset(self):
        # email = self.request.query_params.get('email')
        # user = self.request.user if self.request.user.is_authenticated else None
        locs = Location.objects.filter(featured=True)
        return locs
