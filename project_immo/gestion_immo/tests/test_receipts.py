import pytest
from django.test import TestCase
from django.urls import reverse
from datetime import date
from ..views import receipt, render_pdf_view
from ..models import Apartment, Occupant, Contract, Payment, Receipt

# MODEL TEST - HAS TO PASS generate the receipt

@pytest.mark.django_db 
def test_generate_receipt():
    occupant = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
    apartment = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)

    contract = Contract.objects.create(apartment=apartment, occupant=occupant)
    start_date = ('2023-08-01')
    end_date = ('2023-11-30')

    receipt = Receipt.objects.create(contract=contract, start_date=start_date, end_date=end_date)

    # assert receipt.contract != ''
    assert receipt.contract == contract
    assert receipt.start_date == start_date
    assert receipt.end_date == end_date

# ROUTE TEST

# class ReceiptRouteTest(TestCase):
#     @pytest.mark.django_db
#     def test_receipt_page(self):
#         receipt_url = reverse('receipt')
#         response = self.client.get(receipt_url)
#         assert response.status_code == 200
#         assert response.context['request'].path == '/receipt/'




