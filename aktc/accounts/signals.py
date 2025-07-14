from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from aktcUI.models import Customer


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email)
        Customer.objects.create(
            user=instance, firstname=instance.first_name, surname=instance.last_name,
            email=instance.email)
