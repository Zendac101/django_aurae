from django.contrib import admin
from .models import Core_userProfile, UserProfile_role
# Register your models here.

admin.site.register([Core_userProfile, UserProfile_role])
