from rest_framework.views import APIView
from datetime import timedelta, datetime

from django.shortcuts import render
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import (
    Payment, PaymentMethod, Booking, Review,
    Feedback, Trip, Location, Customer, Route,
    BusDetail, SupportTicket
)
from .serializers import (
    SupportTicketSerializer, CUserserializer,
    BookingCreateSerializer, PaymentSerializer,
    BookingListSerializer, RegisterSerializer,
    FeedbackSerializer, ReviewSerializer,
    TripSerializer, LocationSerializer,
)

from django.contrib.auth import get_user_model


def home(request):
    return render(request, 'home.html', {})


User = get_user_model()

# views.py


class PaymentStatusAPIView(APIView):
    def get(self, request, booking_id):

        payment = Payment.objects.filter(
            booking__booking_id=booking_id).first()
        if not payment:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        print(booking_id, payment, payment.status)
        return Response({"status": payment.status})


class CUserDetailView(generics.RetrieveAPIView):
    serializer_class = CUserserializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        print("User:", request.user)
        print("Auth:", request.auth)
        return self.retrieve(request, *args, **kwargs)


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []


class PaymentHistoryAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(booking__customer__user=self.request.user).order_by("-created")


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    # this allows update via booking_id from frontend
    lookup_field = 'booking__booking_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_method = request.data.get("method")
        # new_method = request.data.get("method")

        if not new_method:
            return Response({"error": "No method provided"}, status=400)

        new_method = PaymentMethod.objects.filter(name=new_method).first()
        instance.method = new_method
        # still in pending as only the payment method was updated
        instance.booking.status = 'pending'
        instance.save()

        # at pay, payment.status will be confirmed

        if new_method == "transfer":
            return Response({"redirect": "/pay/transfer/"})
        elif new_method == "card":
            return Response({"redirect": "/pay/card/"})

        # Optional: redirect or simulate route logic based on method
        return Response(PaymentSerializer(instance).data)


class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer
    permission_classes = []
    default_method = PaymentMethod.objects.filter(is_default=True).first()

    def create(self, request, *args, **kwargs):
        print('REQUEST', request.data)

        trip_id = request.data.pop("trip_id", None)
        customer_email = request.data.get("email", None)
        from_location = request.data.pop("location_from", None)
        to_destination = request.data.pop("destination_to", None)

        trip = Trip.objects.filter(trip_id=trip_id).first()
        customer_user, _ = Customer.objects.get_or_create(email=customer_email)

        booked_route = Route.objects.filter(
            from_location__bus_stop=from_location, to_destination__bus_stop=to_destination).first()
        bus_detail = BusDetail.objects.all().first()
        location_from = Location.objects.filter(bus_stop=from_location).first()
        location_to = Location.objects.filter(bus_stop=to_destination).first()
        print('LOCATIONS OBJECTS?', type(location_from), type(location_to))
        print('LOCATIONS STRINGS?', from_location, to_destination,
              type(from_location), type(to_destination))

        print('DERIVED VARS?', "trip_id", trip_id, "customer_user", customer_user,
              "booked_route", booked_route, "bus_detail", bus_detail, 'location_from',
              location_from, "location_to", location_to)

        if not trip:
            return Response({"error": "Trip not found"}, status=404)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for k, v in serializer.validated_data.items():
            print(f"{k}: {v} ({type(v)})")

        # ✅ Save the booking with a resolved Trip FK
        booking = serializer.save(
            trip=trip, customer=customer_user, booked_route=booked_route,
            bus_detail=bus_detail, location_from=location_from, destination_to=location_to,
            status='confirmed'  # but not "completed" as payment completes it
        )

        print()

        print("Booking Api SECOND", serializer)
        # Calculate fare
        fare_per_seat = booking.trip.route.fare or 4000
        total_fare = float(fare_per_seat * booking.num_of_pass)
        print("fare_per_seat", fare_per_seat)
        print("total_fare", total_fare)

        # return
        # Create payment

        payment_deadline = booking.book_created_at + \
            timedelta(hours=1, minutes=40)

        Payment.objects.create(
            booking=booking,
            amount=total_fare,
            method=PaymentMethod.objects.filter(
                is_default=True).first(),
            payment_deadline=payment_deadline,
            status="pending"
        )

        # Custom summary
        summary = {
            "from": {
                "state": trip.route.from_location.state,
                "stop": trip.route.from_location.bus_stop,
            },
            "to": {
                "state": trip.route.to_destination.state,
                "stop": trip.route.to_destination.bus_stop,
            },
            "departure_date": trip.trip_departure_date,
            "departure_time": trip.trip_departure_time,
            "seats": booking.num_of_pass,
            "fare_per_seat": fare_per_seat,
            "total_fare": total_fare,
        }

        return Response({
            "booking_id": booking.booking_id,
            "trip_summary": summary,
            "status": booking.status,
        }, status=201)

    # def create(self, request, *args, **kwargs):
    #     trip_id = request.data['trip_id']
    #     fare = request.data['trip_id'].pop('fare')  # json not dict
    #     trip = Trip.objects.filter(trip_id=trip_id).first()
    #     serializers = self.get_serializer(data=request.data)
    #     serializers.trip = trip

    #     print()
    #     print('request.data', request.data, trip)
    #     print()
    #     print('serializer Exception', serializer)

    #     serializer.is_valid(raise_exception=True)
    #     booking = serializer.save()

    #     # bus = booking.bus_detail.bus
    #     # driver = booking.bus_detail.driver
    #     validated_data = kwargs['validated_data']
    #     fare_per_seat = fare
    #     num_of_pass = validated_data['num_of_pass']

    #     # fare_per_seat = getattr(bus, 'fare', 5000)
    #     total_fare = fare_per_seat * num_of_pass

    #     # Create a pending payment record
    #     Payment.objects.create(
    #         booking=booking,
    #         amount=total_fare,
    #         payment_method=None,  # to be updated at payment stage
    #         payment_date=timezone.now(),
    #         payment_due=timezone.now() + timedelta(hours=1),
    #         status="Pending"
    #     )

    #     validated_data['trip'] = Trip.objects.get(
    #         trip_departure_date=validated_data['departure_date'],
    #         trip_departure_time=validated_data['departure_time'],
    #         route__location_from=validated_data['location_from'],
    #         route__destination_to=validated_data['destination_to'],
    #     )

    #     # Summary response
    #     summary = {
    #         "location_from": booking.location_from.bus_stop,
    #         "destination_to": booking.destination_to.bus_stop,
    #         "departure_date": booking.departure_date.strftime("%Y-%m-%d"),
    #         "departure_time": booking.departure_time.time,
    #         "seats": booking.num_of_pass,
    #         "fare_per_seat": fare_per_seat,
    #         "total_fare": total_fare,
    #         "num_of_pass": num_of_pass,
    #         # "bus_number": bus.bus_number,
    #         # "driver_name": driver.driver_name
    #     }

    #     return Response({
    #         "booking_id": booking.booking_id,
    #         "trip_summary": summary,
    #         "status": "confirmed"
    #     }, status=status.HTTP_201_CREATED)


class LocationListAPIView(generics.ListAPIView):
    serializer_class = LocationSerializer
    permission_classes = []  # You can make this IsAuthenticated later if needed
    queryset = Location.objects.all()

    # def get_queryset(self):
    #     # email = self.request.query_params.get('email')
    #     # user = self.request.user if self.request.user.is_authenticated else None

    #     if user:
    #         return Booking.objects.filter(email=user.email).order_by('-book_created')
    #     elif email:
    #         return Booking.objects.filter(email=email).order_by('-book_created')
    #     else:
    #         return Booking.objects.all().order_by('-book_created')


class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = []  # You can make this IsAuthenticated later if needed

    def get_queryset(self):
        email = self.request.query_params.get('email')
        user = self.request.user if self.request.user.is_authenticated else None

        if user:
            return Booking.objects.filter(email=user.email).order_by('-book_created')
        elif email:
            return Booking.objects.filter(email=email).order_by('-book_created')
        else:
            return Booking.objects.all().order_by('-book_created')


class FeedbackListAPIView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = []  # Allow anonymous for now

    def get_queryset(self):
        email = self.request.query_params.get('email')
        user = self.request.user if self.request.user.is_authenticated else None

        print()
        print()
        print("email=", email)
        print()
        print()

        if email:
            return Feedback.objects.filter(user__email=email).order_by('-submitted_at')
        elif user:
            return Feedback.objects.filter(user=user).order_by('-submitted_at')
        else:
            return Feedback.objects.none()  # .order_by('-submitted_at')


class FeedbackCreateAPIView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = []  # Allow anonymous for now

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        booking_id = request.data.get("booking")
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        # Ensure feedback isn't duplicated
        if Feedback.objects.filter(booking=booking).exists():
            return Response({"error": "Feedback already submitted for this booking"}, status=400)

        # Ensure trip is completed and within 24hrs
        if booking.trip.status != "completed":
            return Response({"error": "Trip is not yet completed"}, status=400)

        trip_datetime = timezone.make_aware(
            datetime.combine(booking.departure_date, booking.departure_time)
        )

        now = timezone.now()
        if now > trip_datetime + timedelta(hours=24):
            return Response({"error": "Feedback window has expired"}, status=400)

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


class TripListAPIView(generics.ListAPIView):
    serializer_class = TripSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')
        from_ = self.request.query_params.get('from')
        to_ = self.request.query_params.get('to')
        print('Date', date, "From", from_, "To", to_)

        queryset = Trip.objects.all()

        if date:
            queryset = queryset.filter(trip_departure_date=date)
        if from_ and to_:
            queryset = queryset.filter(
                route__from_location__state=from_, route__to_destination__state=to_)

        # print('queryset', [i.trip_departure_time for i in queryset])
        return queryset.order_by('trip_departure_time')


class SupportTicketCreateAPIView(generics.CreateAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = []  # open to all


class TripLiveLocationAPIView(generics.ListAPIView):
    def get(self, request, trip_id):
        try:
            trip = Trip.objects.get(trip_id=trip_id)
            return Response({
                "trip_id": trip.trip_id,
                "latitude": trip.latitude,
                "longitude": trip.longitude,
                "origin_lat": trip.route.from_location.lat,
                "origin_lng": trip.route.from_location.lng,
                "dest_lat": trip.route.to_destination.lat,
                "dest_lng": trip.route.to_destination.lng,


                # "origin_lat": trip.route.route_from.lat,
                # "origin_lng": trip.route.route_from.lng,
                # "dest_lat": trip.route.route_to.lat,
                # "dest_lng": trip.route.route_to.lng,
            })
        except Trip.DoesNotExist:
            return Response({"error": "Trip not found"}, status=404)
