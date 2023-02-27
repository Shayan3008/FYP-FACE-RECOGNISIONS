from django.db import models

# Create your models here.

class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()