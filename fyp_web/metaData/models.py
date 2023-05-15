from django.db import models

from cameras.models import Camera
from users.models import Users

# Create your models here.
class metadata(models.Model):
    camera_id = models.ForeignKey(Camera,null=False,on_delete=models.CASCADE)
    created_at = models.TimeField(auto_now_add=True)
    # user_id = models.ForeignKey(Users, null=False, on_delete = models.CASCADE)
    video_name = models.CharField(null = False, max_length= 200)