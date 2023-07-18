from django.db import models

# Create your models here.

class Apartment(models.Model):
    address = models.CharField(max_length=200)
    address_complement = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    charges_price = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_price = models.DecimalField(max_digits=10, decimal_places=2)

class Occupant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

class Contract(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    occupant = models.OneToOneField(Occupant, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True)

