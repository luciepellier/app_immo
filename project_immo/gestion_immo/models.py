from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.

class Apartment(models.Model):
    address = models.CharField(max_length=200)
    address_complement = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    charges_price = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.address} {self.address_complement}, {self.postal_code} {self.city}"

class Occupant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    
class Agency(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}, {self.city}"

class Contract(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True, related_name="contracts")
    start_date = models.DateField(default=datetime.now, blank=False)
    end_date = models.DateField(blank=True, null=True)
    deposit = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.occupant.last_name} {self.occupant.first_name}  /  {self.apartment.address} {self.apartment.address_complement}, {self.apartment.postal_code} {self.apartment.city}"

class ItemsList(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now, blank=False)
    class ListType(models.TextChoices):
        ENTRÉE = 'Entrée', _('Entrée')
        SORTIE = 'Sortie', _('Sortie')
    list_type = models.CharField(max_length=6, choices=ListType.choices, default=ListType.ENTRÉE, null=False)
    comments = models.TextField()

class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=datetime.now)
    class PaymentSource(models.TextChoices):
        LOCATAIRE = 'Locataire', _('Locataire')
        AUTRE = 'CAF', _('CAF')
    source = models.CharField(max_length=25, choices=PaymentSource.choices, default='Locataire', null=False)
    rental = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.00)

    @property
    def total(self):
        return self.rental + self.charges

class Receipt(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)


