
from django.urls import path
from . import views




urlpatterns = [

    path("support/create/", views.SupportTicketCreateAPIView.as_view(),
         name="support-create"),
    path('reviews/', views.PublicReviewListAPIView.as_view(), name='review-list'),
    path('reviews/create/', views.ReviewCreateAPIView.as_view(), name='review-create'),
    path('feedbacks/', views.FeedbackListAPIView.as_view(), name='feedback-list'),
    path('feedbacks/create/', views.FeedbackCreateAPIView.as_view(),
         name='feedback-create'),
]
