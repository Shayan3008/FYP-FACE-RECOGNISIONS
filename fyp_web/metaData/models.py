from django.db import models

from cameras.models import Camera

# Create your models here.
class metadata(models.Model):
    camera_id = models.ForeignKey(Camera,null=False,on_delete=models.CASCADE)
    created_at = models.TimeField(auto_now_add=True)
