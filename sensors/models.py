from django.db import models


class location(models.Model):
    zipcode = models.IntegerField(
        primary_key=True, unique=True, db_column='zipcode')
    loc_name = models.CharField(max_length=255, db_column="location_name")
    loc_type = models.CharField(max_length=255, db_column='loc_type')

    class Meta:
        managed = True
        db_table = 'pollutant_data"."locations'


class pollutant_data(models.Model):
    zipcode = models.ForeignKey(
        location, on_delete=models.CASCADE, db_column='zipcode')

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


class SensorReading(models.Model):
    zipcode = models.ForeignKey(
        location, on_delete=models.CASCADE, db_column='zipcode')
    aqi = models.FloatField(null=True, blank=True)

    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    pm25 = models.FloatField(null=True, blank=True)
    pm10 = models.FloatField(null=True, blank=True)
    co = models.FloatField(null=True, blank=True)
    no2 = models.FloatField(null=True, blank=True)

    classification = models.CharField(max_length=50, null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'pollutant_data"."unverified_readings'


class SavedModel(models.Model):
    model_name = models.CharField(max_length=100, unique=True)
    model_data = models.BinaryField()

    def __str__(self):
        return self.model_name

    class Meta:
        managed = True
        db_table = 'pollutant_data"."machine_learning_model'
