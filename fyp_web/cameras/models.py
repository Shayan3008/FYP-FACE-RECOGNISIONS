from django.db import models
from coordinates.models import Coordinates
# Create your models here.
class Camera(models.Model):
    cameraLocation = models.OneToOneField(Coordinates, on_delete=models.CASCADE)