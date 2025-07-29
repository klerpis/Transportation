from django.shortcuts import render

from rest_framework import generics #, status
from .models import Location
from .serializers import LocationSerializer

class LocationListAPIView(generics.ListAPIView):
    serializer_class = LocationSerializer
    permission_classes = []  # You can make this IsAuthenticated later if needed
    queryset = Location.objects.all()

    # def get_queryset(self):
    #     # email = self.request.query_params.get('email')
    #     # user = self.request.user if self.request.user.is_authenticated else None

    #     if user:
    #         return Booking.objects.filter(email=user.email).order_by('-book_created_at')
    #     elif email:
    #         return Booking.objects.filter(email=email).order_by('-book_created_at')
    #     else:
    #         return Booking.objects.all().order_by('-book_created_at')

