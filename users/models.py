from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth import get_user_model

from django.dispatch import receiver

from recipes.models import Recipe


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Recipe, related_name='favorited_by')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
