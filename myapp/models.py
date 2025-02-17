from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.



class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null =True) 
    email = models.EmailField(unique= True)


    def __str__(self):
        return "{}".format(self.email)
