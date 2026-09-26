from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

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

    zipcode = models.IntegerField(
        primary_key=True, db_column='zipcode', unique=True)

    municipality = models.CharField(max_length=255, db_column='municipality')

    region = models.CharField(max_length=45, db_column='region')

    class Meta:
        managed = False
        db_table = 'pollutant_data"."locations'


class zipcode(models.Model):
    zipcode = models.CharField(max_length=100)


class pollutant_data(models.Model):
    zipcode = models.ForeignKey(
        locationData, on_delete=models.CASCADE, db_column='zipcode')

    date = models.DateField(db_column='date')

    aqi = models.IntegerField(db_column='aqi')

    so2 = models.DecimalField(max_digits=6, decimal_places=2, db_column='so2')
    co = models.DecimalField(max_digits=6, decimal_places=2, db_column='co')
    o3 = models.DecimalField(max_digits=6, decimal_places=2, db_column='o3')
    pm10 = models.DecimalField(
        max_digits=6, decimal_places=2, db_column='pm10')
    nox = models.DecimalField(max_digits=6, decimal_places=2, db_column='nox')
    aqi_pm25 = models.DecimalField(
        max_digits=6, decimal_places=2, db_column='aqi_pm2.5')
    aqi_pm10 = models.DecimalField(
        max_digits=6, decimal_places=2, db_column='aqi_pm10')
    pm25 = models.DecimalField(
        max_digits=6, decimal_places=2, db_column='pm2.5')

    class Meta:
        managed = False
        db_table = 'pollutant_data"."pollutant_values'
