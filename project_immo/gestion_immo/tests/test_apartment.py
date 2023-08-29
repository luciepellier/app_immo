import pytest
from django.urls import reverse
from ..models import Apartment

# VIEWS TESTS

@pytest.mark.django_db
def test_apartment_list_view(client):
        apartmentlist_url = reverse('apartment_list')
        response = client.get(apartmentlist_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/apartment/list/'

@pytest.mark.django_db
def test_apartment_form_view(client):
        url = reverse('apartment_insert')
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/apartment/'
        # assert 'Ajouter / Modifier un Appartement' in str(response.content)

@pytest.mark.django_db
def test_apartment_update_view(client):
        apartment = Apartment.objects.create(id=123, address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        url = reverse('apartment_update', args=[apartment.id])
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/apartment/123/'      

@pytest.mark.django_db
def test_apartment_delete_view(client):
        apartment = Apartment.objects.create(id=123, address='15 rue de la République', address_complement='3-2', city='Lyon', 
                                postal_code='69005', rental_price=1200.00, charges_price=400.00, deposit_price=2400.00)
        url = reverse('apartment_delete', args=[apartment.id])
        response = client.get(url)
        assert response.status_code == 302



