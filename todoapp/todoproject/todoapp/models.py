from django.db import models

# Create your models here.
class Register(models.Model):
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    email = models.EmailField()
    password = models.CharField(max_length=50, null=False)
    password2 = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name
    
class Todo(models.Model):
    task = models.CharField(max_length=500, null=False)