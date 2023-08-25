import pytest
from django.test import TestCase
from django.urls import reverse
from datetime import date
from ..models import Apartment, Occupant, Contract, Agency

# MODEL TEST - HAS TO PASS : given 2 apartments and 1 occupant, the occupant can rent the 2 apartments (= agree 2 contracts)

@pytest.mark.django_db
def test_one_occupant_has_two_contract_apartments():
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        apartment_2 = Apartment.objects.create(address='25 rue de la République', address_complement='2-3', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        agency_1 = Agency.objects.create(name='Agence 1', city='Rosas')
        start_date = date.today()
        contract_duration = start_date.year + 3
        end_date = start_date.replace(contract_duration)
        
        contract_1 = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, agency=agency_1, 
                                start_date=start_date, end_date=end_date)
        contract_2 = Contract.objects.create(apartment=apartment_2, occupant=occupant_1, agency=agency_1, 
                                start_date=start_date, end_date=end_date)

        assert contract_1.occupant.first_name == contract_2.occupant.first_name, 'the 2 contracts have not the same occupant first name'
        assert contract_1.occupant.last_name == contract_2.occupant.last_name, 'the 2 contracts have not the same occupant first name'
        assert contract_1.occupant == contract_2.occupant, 'the 2 contracts have not the same occupant id'
        assert contract_1.apartment != contract_2.apartment, 'the 2 apartments have the same id'

# MODEL TEST - HAS TO FAIL : add a new contract for an apartment when a contract already exists for this apartment id

@pytest.mark.django_db
def test_not_save_contract_when_apartment_has_already_one():
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        agency_1 = Agency.objects.create(name='Agence 1', city='Rosas')
        start_date = date.today()
        contract_duration = start_date.year + 3
        end_date = start_date.replace(contract_duration)

        contract_1 = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, agency=agency_1, 
                                start_date=start_date, end_date=end_date)

        assert Contract.objects.create(apartment=apartment_1, occupant=occupant_1, agency=agency_1, 
                                start_date=start_date, end_date=end_date)
        

# MODEL TEST - HAS TO FAIL : a contract with created with an end date similar or inferior than start date

@pytest.mark.django_db 
def test_not_save_contract_when_invalid_end_date():
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        agency_1 = Agency.objects.create(name='Agence 1', city='Rosas')
        start_date = date.today()
        contract_duration = start_date.year - 3
        end_date = start_date.replace(contract_duration)
        
        contract_1 = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, agency=agency_1, 
                                start_date=start_date, end_date=end_date) 

        assert contract_1.end_date >= contract_1.start_date, 'contract end date cannot be inferior or equal to start date'

# MODEL TEST - HAS TO FAIL : a contract cannot be saved without ticking the "deposit payment done" case

@pytest.mark.django_db 
def test_not_save_contract_when_deposit_payment_not_done():
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        agency_1 = Agency.objects.create(name='Agence 1', city='Rosas')
        start_date = date.today()
        contract_duration = start_date.year + 1
        end_date = start_date.replace(contract_duration)

        contract_1 = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, agency=agency_1, 
                                start_date=start_date, end_date=end_date)
        
        assert contract_1.deposit == False, 'deposit payment is required as True to save the contract'

# ROUTE TEST

class ContractRouteTest(TestCase):
    @pytest.mark.django_db
    def test_contract_list_page(self):
        contractlist_url = reverse('contract_list')
        response = self.client.get(contractlist_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/contract/list/'

