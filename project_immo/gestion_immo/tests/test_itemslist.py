import pytest
from django.test import TestCase
from django.urls import reverse
from datetime import date
from ..models import Apartment, Occupant, Contract, Agency, ItemsList

# VIEWS TESTS

@pytest.mark.django_db
def test_itemslist_list_view(client):
        itemslist_url = reverse('itemslist_list')
        response = client.get(itemslist_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/itemslist/list/'

@pytest.mark.django_db
def test_itemslist_form_view(client):
        url = reverse('itemslist_insert')
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/itemslist/'

@pytest.mark.django_db
def test_itemslist_update_view(client):

        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        start_date = date.today()
        contract = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, start_date=start_date)

        date_1 = date.today()
        list_type = 'Entrée'
        comments = 'OK'
        itemslist = ItemsList.objects.create(id=123,contract=contract, date=date_1, list_type=list_type, comments=comments)    
        
        url = reverse('itemslist_update', args=[itemslist.id])
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/itemslist/123/'      

@pytest.mark.django_db
def test_itemslist_delete_view(client):

        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        start_date = date.today()
        contract = Contract.objects.create(id=123, apartment=apartment_1, occupant=occupant_1, start_date=start_date)

        date_1 = date.today()
        list_type = 'Entrée'
        comments = 'OK'
        itemslist = ItemsList.objects.create(contract=contract, date=date_1, list_type=list_type, comments=comments)    
        
        url = reverse('itemslist_delete', args=[itemslist.id])
        response = client.get(url)

        assert response.status_code == 302

# MODEL TEST

@pytest.mark.django_db 
def test_not_create_two_itemslist_with_same_list_type():
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        agency_1 = Agency.objects.create(name='Agence 1', city='Rosas')
        start_date = date.today()
        contract_duration = start_date.year + 3
        end_date = start_date.replace(contract_duration)
        contract_1 = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, agency=agency_1, 
                                start_date=start_date, end_date=end_date, deposit=True)
        
        date_1 = date.today()
        list_type = 'Entrée'
        comments = 'OK'

        itemslist_1 = ItemsList.objects.create(contract=contract_1, date=date_1, list_type=list_type, comments=comments)
        assert itemslist_1.save() == None, 'cannot create 2 itemslist with the same list type'

# ROUTE TEST

class ItemsListRouteTest(TestCase):
    @pytest.mark.django_db
    def test_items_list_page(self):
        itemslist_url = reverse('itemslist_list')
        response = self.client.get(itemslist_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/itemslist/list/'

