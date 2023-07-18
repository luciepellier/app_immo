from datetime import date
from django.test import TestCase
from .models import Apartment, Occupant, Contract

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
        # agrees the occupant, apartment, start and end date of the rental contract
        self.occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        self.apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        self.start_date = date.today()
        contract_duration = self.start_date.year + 3
        self.end_date = self.start_date.replace(contract_duration)

    def test_contract_assignement(self):
        # Test in TDD, we check there's no contract created
        self.assertEqual(Contract.objects.count(), 0)
        # We assign the values set up to the contract
        assignement = Contract.objects.create(apartment=self.apartment_1, occupant=self.occupant_1, start_date=self.start_date, end_date=self.end_date)
        # We check there's a contract created 
        self.assertEqual(Contract.objects.count(), 1)
        # We check the contract values are the same as the set up values
        self.assertEqual(assignement.apartment, self.apartment_1)
        self.assertEqual(assignement.occupant, self.occupant_1)
        self.assertEqual(assignement.start_date, self.start_date)
        self.assertEqual(assignement.end_date, self.end_date)
        # We also check with the strings
        self.assertEqual(assignement.apartment.address, '15 rue de la République')
        self.assertEqual(assignement.occupant.first_name, 'Pedro')        



        