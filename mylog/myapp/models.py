from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    name = models.CharField(max_length=30,unique=True)
    email = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name


    