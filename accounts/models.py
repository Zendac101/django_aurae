from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Keep your original profile model if needed

class CoreUserProfileManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)

        # Ensure the user account gets generated cleanly
        user = self.create_user(email, username, password, **extra_fields)

        # Automatically link the permissions to your separate roles and history tables
        from .models import UserProfile_history, UserProfile_role

        UserProfile_role.objects.update_or_create(
            user=user,
            defaults={"is_staff": True,
                      "is_superuser": True, "is_verified": True},
        )
        UserProfile_history.objects.update_or_create(
            user=user, defaults={"is_verified": True}
        )

        return user


class Core_userProfile(AbstractBaseUser):
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    objects = CoreUserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        managed = True
        db_table = 'core_userprofile'

    def __str__(self):
        return f"{self.username}'s Profile"

    @property
    def is_staff(self):
        try:
            return self.roles.is_staff
        except AttributeError:
            return False

    @property
    def is_superuser(self):
        try:
            return self.roles.is_superuser
        except AttributeError:
            return False

    # Required methods for Django Admin permissions checks
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class UserProfile_history(models.Model):
    user = models.OneToOneField(
        Core_userProfile, on_delete=models.CASCADE, related_name='profile_history', primary_key=True)

    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True)

    class Meta:
        managed = True
        db_table = 'user_history'


class UserProfile_role(models.Model):
    user = models.OneToOneField(
        Core_userProfile, on_delete=models.CASCADE, related_name='roles', primary_key=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'user_roles'


# History Table
class ActivityHistory(models.Model):
    user = models.ForeignKey(
        Core_userProfile, on_delete=models.CASCADE, related_name='activity_histories')
    activity_log = models.TextField()
    log_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'user_activityhistory'


@receiver(post_save, sender=Core_userProfile)
def create_user_dependent_profiles(sender, instance, created, **kwargs):
    if created:
        # Automatically insert empty/default data into your separate tables
        UserProfile_history.objects.create(user=instance)
        UserProfile_role.objects.create(user=instance)
