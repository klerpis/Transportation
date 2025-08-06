import uuid
import random
from rest_framework.views import APIView
from datetime import timedelta, datetime

from django.shortcuts import render
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from setupsystem.models import (Location, Route,)

from .models import (
    Payment, PaymentMethod, Booking, 
    Trip, Customer,
    BusDetail
)
from .serializers import (
    CUserserializer,
    BookingCreateSerializer, PaymentSerializer,
    BookingListSerializer, RegisterSerializer,
    TripSerializer
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
    
    def patch(self, request, booking_id):
        print("booking_id", booking_id, request)
        print(request.data)
        print()
        payment_status = request.data.get('status')
        payment = Payment.objects.filter(
            booking__booking_id=booking_id).first()
        if not payment:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        if payment_status and payment_status in ['pending', 'success', 'failed']:
            # payment.booking.status = 'confirmed' if payment_status == 'success' else 'failed'
            payment.status = payment_status
            payment.save()
            # payment.booking.save()
            return Response(PaymentSerializer(payment).data) 



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


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = []
    lookup_field = 'booking_id'

    def get_object(self):
        print("entered thje retrieve", self.kwargs)
        booking_id = self.kwargs.get('booking_id')
        print("booking_id", booking_id)
        return Payment.objects.filter(booking__booking_id=booking_id).first()



class PaymentHistoryAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            return Payment.objects.filter(booking__customer__user=self.request.user).order_by("-created")
        except Exception as e:
            return Payment.objects.none()


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    # this allows update via booking_id from frontend
    lookup_field = 'booking__booking_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_method = request.data.get("method")
        payment_status = request.data.get("status")
        # new_method = request.data.get("method")

        if payment_status and payment_status in ['pending', 'success', 'failed']:
            # instance.booking.status = 'confirmed' if payment_status == 'success' else 'failed'
            instance.status = payment_status
            instance.save()
            return Response(PaymentSerializer(instance).data) 

        if not new_method:
            return Response({"error": "No method provided"}, status=400)

        new_method = PaymentMethod.objects.filter(name=new_method).first()
        instance.method = new_method
        # still in pending as only the payment method was updated
        # instance.booking.status = 'pending'
        instance.save()

        # at pay, payment.status will be confirmed

        if new_method == "transfer":
            return Response({"redirect": "/pay/transfer/"})
        elif new_method == "card":
            return Response({"redirect": "/pay/card/"})

        # Optional: redirect or simulate route logic based on method
        return Response(PaymentSerializer(instance).data)

def generate_id():
    gener = ['dioucbyg', 'ifdcyugd', 'ncidgyu', 'jdcbheu', 'dbh', 'fdu',
    'der', 'd3ex', 'derqr', 'fergry']
    code = str(int(uuid.uuid4()))[:random.randint(1, 9)]
    gen_id = f"{random.choice(gener)}-{code}"
    return code

class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer
    permission_classes = []
    default_method = PaymentMethod.objects.filter(is_default=True).first()

    def create(self, request, *args, **kwargs):
        print('REQUEST', request.data, self.request.user, )
        print("self.request.user.is_authenticated()", self.request.user.is_authenticated)

        trip_id = request.data.pop("trip_id", None)
        customer_email = request.data.get("email", None)
        from_location = request.data.pop("location_from", None)
        to_destination = request.data.pop("destination_to", None)
        user = self.request.user

        
        trip = Trip.objects.filter(trip_id=trip_id).first()
        
        customer_user  = None
        try:
            if user.is_authenticated:
                customer_user = Customer.objects.filter(user=user).first()
            else:

                customer_user = Customer.objects.filter(email=customer_email).first()
                if not customer_user:
                    user = User.objects.create_user(email=instance.email, 
                    username=f"{request.data.get('first_name', '')}{request.data.get('last_name', '')}".lower(), 
                    password=generate_id())
                    customer_user =  Customer.objects.create(user=user, 
                    firstname=request.data.get('first_name', ''), 
                    surname=request.data.get('last_name', ''))

        except Exception as e:
            print("ERRORRRRRRRRR", e)
        finally:
            print("Finally-----", )
            if not customer_user:
                print("Finally all user creation failed" )
                
                customer_user = Customer.objects.create(
                                        email=customer_email,
                                        firstname=request.data.get('first_name', ''),
                                        surname=request.data.get('last_name', ''),)


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



class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]  # You can make this IsAuthenticated later if needed

    def get_queryset(self):
        # email = self.request.query_params.get('email')
        user = self.request.user if self.request.user.is_authenticated else None

        querset = Booking.objects.filter(customer__user=user).first()
        if user:
            # data = querset.filter(customer__user=user).order_by('-book_created_at')
            # print("DATATATQ", data)
            return querset 
        else:
            return Booking.objects.none() 


# elif email:
#     return Booking.objects.filter(email=email).order_by('-book_created_at')


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
        if (not date and not from_ and not to_):
            print(datetime.today().strftime('%Y-%m-%d'))
            print()
            print((date and from_ and to_))
            print()
            print(date)
            queryset = queryset.filter(trip_departure_date=datetime.today().strftime('%Y-%m-%d')) 


        # print('queryset', [i.trip_departure_time for i in queryset])
        return queryset.order_by('trip_departure_time')



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
