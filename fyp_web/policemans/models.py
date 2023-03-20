from django.db import models

from area.models import Area

# Create your models here.
class policeman(models.Model):
    email = models.EmailField( max_length=254,null=False)
    password = models.TextField(null=False)
    area = models.OneToOneField(Area,on_delete=models.CASCADE)
