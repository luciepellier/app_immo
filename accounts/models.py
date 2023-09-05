from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Agency(AbstractUser):
    # name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name}, {self.city}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"