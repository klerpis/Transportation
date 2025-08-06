from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from aktcUI.models import Customer
import uuid
import random

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print()
        print("instance", instance)
        print()
        print()
        # Profile.objects.create(user=instance, email=instance.email)
        Customer.objects.create(
            user=instance, firstname=instance.first_name, surname=instance.last_name,
            email=instance.email)


@receiver(post_save, sender=Customer)
def create_customer_profile(sender, instance, created, **kwargs):
    
    if created:
        Profile.objects.create(user=instance.user, email=instance.email)
        # Customer.objects.create(
        #     user=user, firstname=instance.firstname, surname=instance.surname,
        #     email=instance.email)
