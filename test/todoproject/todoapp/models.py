from django.db import models

# Create your models here.
class Todo(models.Model):
    task = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='In progress')

    def __str__(self):
        return self.task