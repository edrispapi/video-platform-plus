from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # سایر فیلدها

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="profiles")
    name = models.CharField(max_length=64)
    preferences = models.JSONField(default=dict, blank=True)
