import pytest
from django.test import TestCase
from django.urls import reverse
from datetime import date
from gestion_immo.models import Apartment, Occupant, Contract, Agency, Payment

# VIEWS TESTS

@pytest.mark.django_db
def test_payment_list_view(client):
        paymentlist_url = reverse('payment_list')
        response = client.get(paymentlist_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/payment/list/'

@pytest.mark.django_db
def test_payment_form_view(client):
        url = reverse('payment_insert')
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/payment/'
        # assert 'Ajouter / Modifier un Paiement' in str(response.content)

@pytest.mark.django_db
def test_payment_update_view(client):

        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        start_date = date.today()
        contract = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, start_date=start_date)
        payment = Payment.objects.create(id=123, date=date.today(), contract=contract, source='Locataire', rental=1200.00, charges=0)

        url = reverse('payment_update', args=[payment.id])
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/payment/123/'      

@pytest.mark.django_db
def test_payment_delete_view(client):

        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        start_date = date.today()
        contract = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, start_date=start_date)
        payment = Payment.objects.create(id=123, date=date.today(), contract=contract, source='Locataire', rental=1200.00, charges=0)
        url = reverse('payment_delete', args=[payment.id])
        response = client.get(url)

        assert response.status_code == 302

@pytest.mark.django_db
def test_rental_list_view(client):
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        start_date = date.today()
        contract = Contract.objects.create(id=123, apartment=apartment_1, occupant=occupant_1, start_date=start_date)
        # payment_1 = Payment.objects.create(id=123, date=date.today(), contract=contract, source='Locataire', rental=1200.00, charges=0)

        url = reverse('rental_list', args=[contract.id])
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/rental/123/'      

@pytest.mark.django_db
def test_commission_list_view(client):
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        agency_1 = Agency.objects.create(id=123, first_name='ImmoTest', city='Figueras')
        start_date = date.today()
        contract = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, start_date=start_date)
        # payment_1 = Payment.objects.create(date=date.today(), contract=contract, source='Locataire', rental=1200.00, charges=0)

        url = reverse('commission_list', args=[agency_1.id])
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/commission/123/'      

# MODEL TESTS

@pytest.mark.django_db 
def test_rental_payment_superior_than_zero():
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        agency_1 = Agency.objects.create(first_name='Agence 1', city='Rosas')
        start_date = date.today()
        contract_duration = start_date.year + 3
        end_date = start_date.replace(contract_duration)
        contract = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, agency=agency_1, 
                                start_date=start_date, end_date=end_date) 
        payment_1 = Payment.objects.create(id=123, date=date.today(), contract=contract, source='Locataire', rental=1200.00, charges=0)
        
        assert payment_1.rental >= 100, 'rental payment min value is 100'
        assert payment_1.rental != '', 'rental payment cannot be null'
        assert payment_1.charges == 0, 'charges payment can be null'

# ROUTE TEST

class PaymentListRouteTest(TestCase):
    @pytest.mark.django_db
    def test_payment_list_page(self):
        paymentlist_url = reverse('payment_list')
        response = self.client.get(paymentlist_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/payment/list/'