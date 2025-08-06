from .views import PaymentUpdateAPIView, PaymentHistoryAPIView, PaymentRetrieveAPIView
from django.urls import path
from . import views

# from .views import BookingListAPIView


urlpatterns = [
    path('', views.home, name='home'),
    path('bookings/', views.BookingListAPIView.as_view(), name='booking-list'),
    path('bookings/create/', views.BookingCreateAPIView.as_view(),
         name='booking-create'),
    path('trips/', views.TripListAPIView.as_view(), name='trip-list'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('me/', views.CUserDetailView.as_view(), name='user-detail'),
    path("payments/update/<str:booking__booking_id>/",
         PaymentUpdateAPIView.as_view(), name="payment-update"),
         
    path("payment/<str:booking_id>/", PaymentRetrieveAPIView.as_view(),
         name="payment"),
    path("payments/history/", PaymentHistoryAPIView.as_view(),
         name="payment-history"),
    path("payments/status/<str:booking_id>/", views.PaymentStatusAPIView.as_view(),
         name="payment-status"),


]
