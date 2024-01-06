from django.db import models

# Create your models here.


class contact(models.Model):
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    phone = models.IntegerField(null=True)
    message = models.CharField(max_length=500,null=True)

class joiners(models.Model):
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    phone = models.IntegerField(null=True)
    clas = models.CharField(max_length=50, null=True)