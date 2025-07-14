from .views import PaymentUpdateAPIView, PaymentHistoryAPIView
from django.urls import path
from . import views
# from .views import BookingListAPIView


urlpatterns = [
    path('', views.home, name='home'),
    path('bookings/', views.BookingListAPIView.as_view(), name='booking-list'),
    path('bookings/create/', views.BookingCreateAPIView.as_view(),
         name='booking-create'),
    path('reviews/', views.PublicReviewListAPIView.as_view(), name='review-list'),
    path('reviews/create/', views.ReviewCreateAPIView.as_view(), name='review-create'),
    path('feedbacks/', views.FeedbackListAPIView.as_view(), name='feedback-list'),
    path('feedbacks/create/', views.FeedbackCreateAPIView.as_view(),
         name='feedback-create'),
    path('trips/', views.TripListAPIView.as_view(), name='trip-list'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('me/', views.CUserDetailView.as_view(), name='user-detail'),
    path("support/create/", views.SupportTicketCreateAPIView.as_view(),
         name="support-create"),
    path('locations/', views.LocationListAPIView.as_view(), name='locations'),
    path("payments/update/<str:booking__booking_id>/",
         PaymentUpdateAPIView.as_view(), name="payment-update"),
    path("payments/history/", PaymentHistoryAPIView.as_view(),
         name="payment-history"),
    path("payments/status/<str:booking_id>/", views.PaymentStatusAPIView.as_view(),
         name="payment-status"),


]
