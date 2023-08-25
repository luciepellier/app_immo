import pytest
from django.test import TestCase
from django.urls import reverse
from datetime import date
from ..models import Apartment, Occupant, Contract, Agency, Payment

# MODEL TEST - HAS TO PASS : given 1 contract, the rental payment cannot be inferior than 100

@pytest.mark.django_db 
def test_rental_payment_must_be_superior_zero():
        apartment_1 = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        occupant_1 = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        agency_1 = Agency.objects.create(name='Agence 1', city='Rosas')
        start_date = date.today()
        contract_duration = start_date.year + 3
        end_date = start_date.replace(contract_duration)
        
        date_1 = date.today()
        contract_1 = Contract.objects.create(apartment=apartment_1, occupant=occupant_1, agency=agency_1, 
                                start_date=start_date, end_date=end_date) 
        source = 'Locataire'
        rental = 100.00
        charges = 0
        
        payment_1 = Payment.objects.create(date=date_1, contract=contract_1, source=source, rental=rental, charges=charges)
        
        assert payment_1.rental >= 100.00, 'rental payment min value is 100'
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