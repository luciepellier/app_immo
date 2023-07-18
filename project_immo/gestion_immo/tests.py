from datetime import date
from django.test import TestCase
from .models import Apartment, Occupant

# Create your tests here.

class ApartmentTest(TestCase):
    def test_add_apartment(self):
        # Test in TDD, we check there's no apartment created
        self.assertEqual(Apartment.objects.count(), 0)
        # create/add new apartment
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        # test if apartment 1 is created
        self.assertEqual(Apartment.objects.count(), 1)
        self.assertEqual(apartment_1.address, '15 rue de la République')

class OccupantTest(TestCase):
    def test_add_occupant(self):
        # Test in TDD, we check there's no occupant created
        self.assertEqual(Occupant.objects.count(), 0)
        # create/add new occupant
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        # test if occupant 1 is created
        self.assertEqual(Occupant.objects.count(), 1)
        self.assertEqual(occupant_1.first_name, 'Pedro')

class ContractAssigmentTest(TestCase):
    def setUp(self):
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
    def test_occupant_entering_apartment(self):
        self.assertEqual(Contract.objects.count(), 0)

        