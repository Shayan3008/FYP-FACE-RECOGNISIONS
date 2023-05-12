from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(null=False,max_length=100)
    email = models.EmailField( max_length=254,null=False,unique=True)
    password = models.CharField(null=False,max_length=100)

class ForgotPassword(models.Model):
    userId = models.BigIntegerField()
    resetCode = models.CharField(max_length = 6)