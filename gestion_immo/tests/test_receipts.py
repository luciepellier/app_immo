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

    url = reverse('render_pdf_view')
    payload = {
          "contract": contract.id,
          "start_date": "2023-09-03",
          "end_date": "2023-09-04"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = client.post(
        url, 
        data=payload,
        **headers
    )
    assert response.status_code == 200




