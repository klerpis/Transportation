from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, Booking


@receiver(post_save, sender=Payment)
def handle_payment_confirmation(sender, instance, created, **kwargs):
    if instance.status == 'success' and instance.booking.status != 'confirmed':
        instance.booking.status = 'confirmed'
        instance.booking.save()
    if instance.status == 'pending' and instance.booking.status != 'pending':
        instance.booking.status = 'pending'
        instance.booking.save()
    if instance.status == 'failed' and instance.booking.status != 'failed':
        instance.booking.status = 'failed'
        instance.booking.save()
    

@receiver(post_save, sender=Booking)
def handle_booking_confirmation(sender, instance, created, **kwargs):
    if instance.status == 'pending' and hasattr(instance, 'payment') and \
        instance.payment.status != 'pending':
        instance.payment.status = 'pending'
        instance.payment.save()
    if (instance.status == 'confirmed' or instance.status == 'completed') and \
        hasattr(instance, 'payment') and \
        instance.payment.status != 'success': # caused error when in front
        
        instance.payment.status = 'success'
        instance.payment.save()
    if instance.status == 'failed' and hasattr(instance, 'payment') and \
        instance.payment.status != 'failed':

        instance.payment.status = 'failed'
        instance.payment.save()
    