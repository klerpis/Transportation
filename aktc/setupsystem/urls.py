
from django.urls import path
from . import views



urlpatterns = [
    path('locations/', views.LocationListAPIView.as_view(), name='locations'),
    path('featured-locations/', views.FeaturedLocationListAPIView.as_view(), name='featured-locations'),
    
]