from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    friend_request_sent = models.ManyToManyField(User, blank=True, related_name='friend_request_sent')
    friend_request_received = models.ManyToManyField(User, blank=True, related_name='friend_request_received')
    friends_list = models.ManyToManyField(User, blank=True, related_name='friends_list')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
