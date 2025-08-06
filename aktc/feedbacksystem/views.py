from django.shortcuts import render
from .models import Feedback, Review, SupportTicket
from aktcUI.models import Booking

# from rest_framework.views import APIView
from datetime import timedelta, datetime

from django.utils import timezone

from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import (
    FeedbackSerializer,
    ReviewSerializer,
    SupportTicketSerializer
)

# from django.contrib.auth import get_user_model



class FeedbackListAPIView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = []  # Allow anonymous for now

    def get_queryset(self):
        email = self.request.query_params.get('email')
        user = self.request.user if self.request.user.is_authenticated else None

        # print()
        # print()
        # print("email=", email)
        # print(f"USER ID OOOOH {self.request.user}", self.request.user if self.request.user.is_authenticated else None)
        # print()
        # print()

        if email:
            print('email data')
            data = Feedback.objects.filter(user__email=email).order_by('-submitted_at')
            print('email data', data)
            return data # .order_by('-submitted_at')
        elif user:
            print('iser data')
            data = Feedback.objects.filter(user__user=user).order_by('-submitted_at')
            print('iser data', data)
            return data    # .order_by('-submitted_at')
        else:
            print('no data')
            data = Feedback.objects.none()
            print('no data', data)
            return data   #    .order_by('-submitted_at')


class FeedbackCreateAPIView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = []  # Allow anonymous for now

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        booking_id = request.data.get("booking")
        try:
            booking = Booking.objects.filter(booking_id=booking_id).first()
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        # Ensure feedback isn't duplicated
        if Feedback.objects.filter(trip_books=booking).exists():
            return Response({"error": "Feedback already submitted for this booking"}, status=400)

        # # Ensure trip is completed and within 24hrs
        # if booking.trip.status != "completed":
        #     return Response({"error": "Trip is not yet completed"}, status=400)

        # trip_datetime = timezone.make_aware(
        #     datetime.combine(booking.departure_date, booking.departure_time)
        # )

        # now = timezone.now()
        # if now > trip_datetime + timedelta(hours=24):
        #     return Response({"error": "Feedback window has expired"}, status=400)

        # All good, create feedback
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = []


class PublicReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = []
    queryset = Review.objects.filter(published=True).order_by('-submitted_at')


class SupportTicketCreateAPIView(generics.CreateAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = []  # open to all

