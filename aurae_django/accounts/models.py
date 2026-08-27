from django.db import models
from django.contrib.auth.models import User


# Keep your original profile model if needed


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# History Table
class ActivityHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='activity_histories')
    activity_log = models.TextField()
    log_datetime = models.DateTimeField(auto_now_add=True)
