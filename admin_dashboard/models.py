from django.db import models

# Create your models here.


class activityHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    activity_log = models.TextField(max_length=255)
    log_datetime = models.DateTimeField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = '"public"."user_activityhistory"'


class locationData(models.Model):

    site_id = models.IntegerField(primary_key=True, db_column='site_id')

    site_name = models.CharField(max_length=255, db_column='site_name')

    county = models.CharField(max_length=45, db_column='county')

    class Meta:
        managed = False
        db_table = '"pollutant_data"."location"'  # The exact table name in your schema


class site_ids(models.Model):
    site_id = models.CharField(max_length=100)


class pollutant_data(models.Model):
    site_id = models.ForeignKey(
        site_ids, on_delete=models.CASCADE, db_column='site_id')

    date = models.DateField(db_column='date')
    time = models.IntegerField(db_column='time')
    aqi = models.IntegerField(db_column='aqi')
    status = models.CharField(max_length=100)
    so2 = models.DecimalField(max_digits=6, decimal_places=2, db_column='so2')
    co = models.DecimalField(max_digits=6, decimal_places=2, db_column='co')
    o3 = models.DecimalField(max_digits=6, decimal_places=2, db_column='o3')
    no2 = models.DecimalField(max_digits=6, decimal_places=2, db_column='no2')
    nox = models.DecimalField(max_digits=6, decimal_places=2, db_column='nox')
    no = models.DecimalField(max_digits=6, decimal_places=2, db_column='no')

    class Meta:
        managed = False
        db_table = '"pollutant_data"."pollutant_values"'
