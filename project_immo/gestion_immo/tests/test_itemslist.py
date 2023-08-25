import pytest
from django.test import TestCase
from django.urls import reverse
from datetime import date
from ..models import Apartment, Occupant, Contract, Agency, ItemsList

# MODEL TEST - HAS TO FAIL : given 1 itemslist with list type 'Entrée' we cannot save another Entrée list type for this contract

@pytest.mark.django_db 
def test_not_save_itemslist_when_listtype_already_exists():
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

        assert itemslist_1.save(), 'cannot save 2 itemslist with the same list type'

# ROUTE TEST

class ItemsListRouteTest(TestCase):
    @pytest.mark.django_db
    def test_items_list_page(self):
        itemslist_url = reverse('itemslist_list')
        response = self.client.get(itemslist_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/itemslist/list/'

