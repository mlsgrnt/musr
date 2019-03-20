from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


# Create a profile for a user when a new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()
