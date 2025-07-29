from django.db import models
from aktcUI.models import Customer, Booking

# Create your models here.

class Feedback(models.Model):

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    rating = models.PositiveIntegerField()  # e.g. 1–5 stars
    submitted_at = models.DateTimeField(auto_now_add=True)
    trip_books = models.ForeignKey(Booking, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-submitted_at']

    def is_valid_window(self):
        return timezone.now() <= self.booking.departure_date + timedelta(hours=48)

    def __str__(self):
        return f"Feedback for {self.trip_books.booking_id}"


class Review(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    published = models.BooleanField(default=False)  # admin approves
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name}"

class SupportTicket(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} ({'✓' if self.resolved else '✗'})"

