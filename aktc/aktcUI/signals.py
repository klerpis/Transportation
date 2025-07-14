from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment


@receiver(post_save, sender=Payment)
def handle_payment_confirmation(sender, instance, created, **kwargs):
    if instance.status == "confirmed":
        booking = instance.booking
        booking.status = "completed"
        booking.save()

        print(
            f"Booking {booking.booking_id} marked as paid/completed via signal.")
