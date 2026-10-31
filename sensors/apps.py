from django.apps import AppConfig
import os
import threading


class SensorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sensors'
