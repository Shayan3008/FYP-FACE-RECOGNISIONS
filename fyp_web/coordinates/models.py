from django.db import models

from area.models import Area

# Create your models here.

class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    area = models.ForeignKey(Area,on_delete=models.CASCADE,null=False)