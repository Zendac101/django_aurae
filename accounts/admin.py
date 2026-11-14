from django.contrib import admin
from .models import Core_userProfile, UserProfile_role, ActivityHistory
# Register your models here.


@admin.register(ActivityHistory)
class ActivityHistory(admin.ModelAdmin):
    list_display = (
        'user',
        'activity_log',
        'log_datetime'
    )

    list_filter = (
        'activity_log',
        'log_datetime'
    )


@admin.register(UserProfile_role)
class UserRoles(admin.ModelAdmin):
    list_display = (
        'user',
        'is_superuser',
        'is_staff',
        'is_verified'
    )

    list_filter = (
        'is_superuser',
        'is_staff',
        'is_verified'
    )


@admin.register(Core_userProfile)
class CoreProfile(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'is_active',
    )

    search_fields = (
        'username',
        'email'
    )
