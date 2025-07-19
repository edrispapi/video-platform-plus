from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="profiles")
    name = models.CharField(max_length=64)
    preferences = models.JSONField(default=dict, blank=True)

class DashboardConfig(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    widgets = models.JSONField(default=dict, blank=True)
