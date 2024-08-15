# models.py
from django.db import models

class SoilHealth(models.Model):
  date = models.DateField()
  soil_moisture = models.FloatField()
  soil_temperature = models.FloatField()
  nitrogen_content = models.IntegerField()
  phosphorus_content = models.IntegerField()
  potassium_content = models.IntegerField()
  soil_ph = models.FloatField()