from datetime import date
from django.test import TestCase
from ..models import Apartment, Occupant, Contract, ItemsList, Payment

# Create your tests here.

# TDD Tests
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

class ItemsListTest(TestCase):
    def setUp(self):
        # Test in TDD, we check there's no items list created
        self.assertEqual(ItemsList.objects.count(), 0)
        # create occupant and apartment for the contract
        self.occupant = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        self.apartment = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        # create the contract
        self.start_date = date.today()
        contract_duration = self.start_date.year + 3
        self.end_date = self.start_date.replace(contract_duration)
        # create items list
        self.contract = Contract.objects.create(apartment = self.apartment, occupant = self.occupant, start_date = self.start_date, end_date = self.end_date)
        self.date = date.today()
        self.comments = 'Meubles légèrement abimés'
        self.list_type = 'Entry'
        self.items_list = ItemsList.objects.create(contract=self.contract, date=self.date, list_type=self.list_type, comments=self.comments)

    def test_add_items_list(self):
        # Test in TDD, we check there's 1 item list created
        self.assertEqual(ItemsList.objects.count(), 1)
        # We check the values and strings are the one entered
        self.assertEqual(self.items_list.contract, self.contract)
        self.assertEqual(self.items_list.date, self.date)
        self.assertEqual(self.items_list.comments, self.comments)
        self.assertEqual(self.items_list.comments, 'Meubles légèrement abimés')
        self.assertEqual(self.items_list.list_type, self.list_type)
        self.assertEqual(self.items_list.list_type, 'Entry')

class PaymentTest(TestCase):

    def setUp(self):
        # Test in TDD, we check there's no payment created
        self.assertEqual(ItemsList.objects.count(), 0)
        # create occupant and apartment for the contract
        self.occupant = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        self.apartment = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        # create the contract
        self.start_date = date.today()
        contract_duration = self.start_date.year + 3
        self.end_date = self.start_date.replace(contract_duration)
        # create payment
        self.contract = Contract.objects.create(apartment=self.apartment, occupant=self.occupant, start_date=self.start_date, end_date=self.end_date)
        self.date = date.today()
        # self.payment_type = 'Rent'
        self.source = 'Locataire'
        self.rental = 1200.00
        self.payment = Payment.objects.create(contract=self.contract, date=self.date, source=self.source, rental=self.rental)

    def test_add_payment(self):
        # We check there's a payment created
        self.assertEqual(Payment.objects.count(), 1)
        # We check the values are the same as the ones entered               
        self.assertEqual(self.payment.contract, self.contract)
        self.assertEqual(self.payment.date, self.date)
        # self.assertEqual(self.payment.payment_type, self.payment_type)
        self.assertEqual(self.payment.source, self.source)
        self.assertEqual(self.payment.rental, self.rental)
