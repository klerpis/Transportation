from django.urls import path
from . import views

urlpatterns = [
    path("user/profile/", views.UserProfileAPIView.as_view(), name="user-profile"),
    # path("user/profile/", views.UserProfileAPIView.as_view(), name="user-profile"),
]
