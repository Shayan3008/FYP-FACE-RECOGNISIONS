from django.db import models
from coordinates.models import Coordinates
# Create your models here.
class Camera(models.Model):
    cameraLocation = models.OneToOneField(Coordinates, on_delete=models.CASCADE)
    cameraClose = models.ForeignKey("self",on_delete=models.CASCADE,null=True,related_name="LEFT_CAMERA")
    cameraClose2 = models.ForeignKey("self",on_delete=models.CASCADE,null=True,related_name="Right_Camera")