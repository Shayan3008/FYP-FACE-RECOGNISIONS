from django.db import models

# Create your models here.
class Area(models.Model):
    Area_name = models.CharField(null=False,max_length=200)