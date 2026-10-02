from django.db import models

# Create your models here.


class locationData(models.Model):

    zipcode = models.IntegerField(
        primary_key=True, db_column='zipcode', unique=True)

    loc_name = models.CharField(max_length=255, db_column='location_name')

    loc_type = models.CharField(max_length=45, db_column='loc_type')

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
