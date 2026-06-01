from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create or update a user profile
    when a User instance is created or saved.
    """
    # Keep this idempotent: existing users without profile are backfilled,
    # and new users always get a profile.
    profile, _ = Profile.objects.get_or_create(user=instance)
    profile.save()
