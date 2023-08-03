from django.db import models
from django.utils.translation import gettext_lazy as _

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

class Contract(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=True, null=True) 

    def __str__(self):
        return f"{self.occupant.last_name} {self.occupant.first_name}  /  {self.apartment.address} {self.apartment.address_complement}, {self.apartment.postal_code} {self.apartment.city}"

class ItemsList(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    class ListType(models.TextChoices):
        ENTRÉE = 'Entrée', _('D\'entrée')
        SORTIE = 'Sortie', _('De sortie')
    list_type = models.CharField(max_length=6, choices=ListType.choices, default=ListType.ENTRÉE, null=False)
    comments = models.TextField()

class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    class PaymentType(models.TextChoices):
        GARANTIE = 'Dépôt de garantie', _('Dépôt de garantie')
        LOYER = 'Loyer (Charges incluses)', _('Loyer (Charges incluses)')
    payment_type = models.CharField(max_length=25, choices=PaymentType.choices, default=PaymentType.LOYER, null=False)
    class PaymentSource(models.TextChoices):
        LOCATAIRE = 'Locataire', _('Locataire')
        AUTRE = 'CAF', _('CAF')
    payment_source = models.CharField(max_length=25, choices=PaymentSource.choices, default=PaymentSource.LOCATAIRE, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)