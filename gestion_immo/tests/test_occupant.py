import pytest
from django.urls import reverse
from ..models import Occupant

# VIEWS TESTS

@pytest.mark.django_db
def test_occupant_list_view(client):
        occupantlist_url = reverse('occupant_list')
        response = client.get(occupantlist_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/occupant/list/'

@pytest.mark.django_db
def test_occupant_form_view(client):
        url = reverse('occupant_insert')
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/occupant/'
        # assert 'Ajouter / Modifier un Locataire' in str(response.content)

@pytest.mark.django_db
def test_contract_update_view(client):
        occupant = Occupant.objects.create(id=123, first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        url = reverse('occupant_update', args=[occupant.id])
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['request'].path == '/occupant/123/'      

@pytest.mark.django_db
def test_contract_delete_view(client):
        occupant = Occupant.objects.create(id=123, first_name='Pedro', last_name='Gonzalez', email='pedrucho@test.com')
        url = reverse('occupant_delete', args=[occupant.id])
        response = client.get(url)
        assert response.status_code == 302

