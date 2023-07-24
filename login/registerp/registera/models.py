from django.db import models

# Create your models here.
class Register(models.Model):
    id =  models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)