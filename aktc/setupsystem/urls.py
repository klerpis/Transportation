
from django.urls import path
from . import views



urlpatterns = [
    path('locations/', views.LocationListAPIView.as_view(), name='locations'),
]