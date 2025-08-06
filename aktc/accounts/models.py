from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    # fullname = models.CharField(max_length=71, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    phonenumber = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # self.fullname = self.fullname if self.fullname else f"{self.user.first_name} {self.user.last_name}"
        return super().save(*args, **kwargs)
