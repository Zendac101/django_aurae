from django.conf import settings
from django.db import models
from django.contrib.auth.models import User  # Points to the auth_user table

# Create your models here.


class activityHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    activity_log = models.TextField(max_length=255)
    log_datetime = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user_id', related_name='activity_logs')

    class Meta:
        managed = False
        db_table = 'user_activityhistory'


class locationData(models.Model):

    site_id = models.IntegerField(
        primary_key=True, db_column='site_id', unique=True)

    site_name = models.CharField(max_length=255, db_column='site_name')

    county = models.CharField(max_length=45, db_column='county')

    class Meta:
        managed = False
        db_table = '"pollutant_data"."location"'  # The exact table name in your schema


class site_ids(models.Model):
    site_id = models.CharField(max_length=100)


class pollutant_data(models.Model):
    site_id = models.ForeignKey(
        locationData, on_delete=models.CASCADE, db_column='site_id')

    date = models.DateField(db_column='date')

    aqi = models.IntegerField(db_column='aqi')

    so2 = models.DecimalField(max_digits=6, decimal_places=2, db_column='so2')
    co = models.DecimalField(max_digits=6, decimal_places=2, db_column='co')
    o3 = models.DecimalField(max_digits=6, decimal_places=2, db_column='o3')
    pm10 = models.DecimalField(
        max_digits=6, decimal_places=2, db_column='pm10')
    nox = models.DecimalField(max_digits=6, decimal_places=2, db_column='nox')
    aqi_pm25 = models.DecimalField(
        max_digits=6, decimal_places=2, db_column='aqi_pm25')
    aqi_pm10 = models.DecimalField(
        max_digits=6, decimal_places=2, db_column='aqi_pm10')
    pm25 = models.DecimalField(
        max_digits=6, decimal_places=2, db_column='pm2.5')

    class Meta:
        managed = False
        db_table = '"pollutant_data"."pollutant_values"'
