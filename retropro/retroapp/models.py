from django.db import models

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    last_login = models.DateTimeField(auto_now=True)

class imageInput(models.Model):
    imageName = models.CharField(max_length=50)
    imageDescription = models.CharField(max_length=500)
    imageField = models.ImageField(upload_to='images/')