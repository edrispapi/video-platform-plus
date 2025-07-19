from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="profiles")
    name = models.CharField(max_length=64, verbose_name=_("name"))
    preferences = models.JSONField(default=dict, blank=True, verbose_name=_("preferences"))

class Channel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_("channel name"))
    subscribers = models.ManyToManyField(CustomUser, related_name="subscribed_channels", blank=True)

class Playlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_("playlist name"))
    videos = models.ManyToManyField('apps.videos.Video', blank=True)
