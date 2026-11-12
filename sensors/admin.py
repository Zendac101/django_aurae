from django.contrib import admin
from .models import pollutant_data, SensorReading
# Register your models here.


@admin.register(SensorReading)
class SensorReadings(admin.ModelAdmin):
    list_display = (
        'zipcode',
        'timestamp',
        'aqi',
        'classification',
        'temperature',
        'humidity',
        'pm25',
        'pm10',
        'co',
        'no2',
        'o3'
    )

    search_fields = (
        'timestamp',
        'classification'
    )

    list_filter = (
        'zipcode',
        'classification'
    )
