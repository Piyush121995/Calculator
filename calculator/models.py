from tkinter.constants import CASCADE

from django.db import models
# from rest_framework.authtoken.admin import User
from django.contrib.auth.forms import UserCreationForm  # Importing the default UserCreationForm
from django.contrib.auth.models import User  # Importing the default User model


# Create your models here.
# class Signup(models.Model):
#     First_name=models.CharField(max_length=50)
#     Last_name=models.CharField(max_length=50)
#     gender = models.CharField(max_length=50)
#     Email=models.EmailField()
#     password=models.CharField('password', max_length=50)


class UserCalculationHistory(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     expression=models.CharField(max_length=250)
     result=models.FloatField()
     Created_at=models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f"{self.user}:{self.expression}={self.result}"




