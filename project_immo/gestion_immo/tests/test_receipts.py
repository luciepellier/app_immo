from datetime import date
import pytest
from django.urls import reverse
from ..models import Apartment, Occupant, Contract, Payment, Receipt

# VIEWS TESTS

@pytest.mark.django_db
def test_receipt_form_view(client):
        url = reverse('receipt_form')
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/receipt/form/'

@pytest.mark.django_db 
def test_render_pdf_receipt_view(client):
    occupant = Occupant.objects.create(first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
    apartment = Apartment.objects.create(address='15 rue de la République', address_complement='3-2', city='Lyon', postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
    contract = Contract.objects.create(apartment=apartment, occupant=occupant)
    payment = Payment.objects.create(date=date.today(), contract=contract, source='Locataire', rental=1200.00, charges=0)
    start_date =  date.today()
    receipt_duration = start_date.month + 3
    end_date = start_date.replace(receipt_duration)

    # receipt = Receipt.objects.create(contract=contract, start_date=start_date, end_date=end_date)

    url = reverse('render_pdf_view')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['request'].path == '/receipt/pdf/'   

    # assert receipt.contract != ''
    # assert receipt.contract == contract
    # assert receipt.start_date == start_date
    # assert receipt.end_date == end_date

# ROUTE TEST

# class ReceiptRouteTest(TestCase):
#     @pytest.mark.django_db
#     def test_receipt_page(self):
#         receipt_url = reverse('receipt')
#         response = self.client.get(receipt_url)
#         assert response.status_code == 200
#         assert response.context['request'].path == '/receipt/'




