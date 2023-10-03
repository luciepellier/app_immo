import pytest
from django.urls import reverse
from datetime import date
from gestion_immo.models import Apartment, Occupant, Contract

# VIEWS TESTS

@pytest.mark.django_db
def test_contract_list_view(client):
        contractlist_url = reverse('contract_list')
        response = client.get(contractlist_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/contract/list/'

@pytest.mark.django_db
def test_contract_form_view(client):
        url = reverse('contract_insert')
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/contract/'
        # assert 'Ajouter / Modifier un Contrat' in str(response.content)

@pytest.mark.django_db
def test_contract_update_view(client):

        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        start_date = date.today()
        contract = Contract.objects.create(id=123, apartment=apartment_1, occupant=occupant_1, start_date=start_date)

        url = reverse('contract_update', args=[contract.id])
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/contract/123/'      

@pytest.mark.django_db
def test_contract_delete_view(client):
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        start_date = date.today()
        contract = Contract.objects.create(id=123, apartment=apartment_1, occupant=occupant_1, start_date=start_date)
        url = reverse('contract_delete', args=[contract.id])
        response = client.get(url)
        assert response.status_code == 302

# MODEL TEST

@pytest.mark.django_db
def test_one_occupant_has_two_contract_apartments():
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        apartment_2 = Apartment.objects.create(address='25 rue de la République', address_complement='2-3', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        start_date = date.today()
        
        contract_1 = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, start_date=start_date)
        contract_2 = Contract.objects.create(apartment=apartment_2, occupant=occupant_1, start_date=start_date)

        assert contract_1.occupant.first_name == contract_2.occupant.first_name, 'the 2 contracts have not the same occupant first name'
        assert contract_1.occupant.last_name == contract_2.occupant.last_name, 'the 2 contracts have not the same occupant first name'
        assert contract_1.occupant == contract_2.occupant, 'the 2 contracts have not the same occupant id'
        assert contract_1.apartment != contract_2.apartment, 'the 2 apartments have the same id'

@pytest.mark.django_db 
def test_is_valid_contract_end_date():
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        start_date = date.today()
        contract_duration = start_date.year + 3
        end_date = start_date.replace(contract_duration)
        contract_1 = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, start_date=start_date, end_date=end_date) 

        assert contract_1.end_date >= contract_1.start_date, 'contract end date has to be inferior or equal to start date'

@pytest.mark.django_db 
def test_deposit_payment_is_true():
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        start_date = date.today()
        contract_1 = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, start_date=start_date)
        
        assert contract_1.deposit == True, 'deposit payment is required as True to save the contract'


