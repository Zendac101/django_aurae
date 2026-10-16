from django.db import models


class SensorReading(models.Model):
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    pm25 = models.FloatField(null=True, blank=True)
    co = models.FloatField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'pollutant_data"."unverified_readings'
