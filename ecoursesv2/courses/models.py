from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# model user
class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

# model category
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    def __str__(self): #override toString method
        return self.name
