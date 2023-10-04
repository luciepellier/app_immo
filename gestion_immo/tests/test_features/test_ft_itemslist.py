from django.test import TestCase
from django.urls import reverse
from accounts.models import Agency
from gestion_immo.models import Apartment, Occupant, Contract, ItemsList
from gestion_immo.forms import ItemsListForm
from datetime import date

class ItemsListFeatureTest(TestCase):
    # Conditions for the test : user created and authenticated in the application
    def create_log_in_agency(self):
        self.username = "johnsmith"
        self.password = "smith_123098"
        self.email = "john@smith.com"
        self.first_name = "John"
        self.last_name = "Smith"
        self.city = "Madrid"

        self.user = Agency.objects.create(username=self.username, email=self.email, first_name=self.first_name, last_name=self.last_name, city=self.city)
        self.user.set_password(self.password)
        self.user.save()

        self.client.force_login(self.user)

    def setUp(self):
        self.create_log_in_agency()      

    def test_user_creates_and_edits_itemslist(self):

        # Check if the user is created and logged in
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.is_authenticated, True) 

        # User enters apartment insert page
        apartment_url = reverse('apartment_insert')
        response = self.client.get(apartment_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/apartment/'

        # User creates an apartment
        self.address = "15 rue de la Republique"
        self.address_complement = "3-2"
        self.city = "Lyon"
        self.postal_code = "69005"
        self.rental_price = 1200.00
        self.charges_price = 400.00
        self.deposit_price = 2400.00

        self.apartment = Apartment.objects.create(address=self.address, address_complement=self.address_complement, city=self.city, postal_code=self.postal_code, rental_price=self.rental_price, charges_price=self.charges_price, deposit_price=self.deposit_price)
        self.apartment.save()
    
        # Check if the apartment is created with the correct data
        self.assertEqual(self.apartment.address, self.address)
        self.assertEqual(Apartment.objects.count(), 1)

        # User enters the occupant insert page
        occupant_url = reverse('occupant_insert')
        response = self.client.get(occupant_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/occupant/'

        # User creates an occupant
        self.first_name = "Tom"
        self.last_name = "Jones"
        self.email = "tom@jones.com"

        self.occupant = Occupant.objects.create(first_name=self.first_name, last_name=self.last_name, email=self.email)
        self.occupant.save()

        # Check if the occupant is created with the correct data
        self.assertEqual(self.occupant.last_name, self.last_name)
        self.assertEqual(Occupant.objects.count(), 1)

        # Load the contract list URL in the "client"
        contractlist_url = reverse('contract_list')
        response = self.client.get(contractlist_url)

        # Check if the page response is 200 & if the path is correct
        # This response should contain "Ajouter un contrat" string, button available only for logged in users 
        assert response.status_code == 200
        assert response.context['request'].path == '/contract/list/'
        assert 'Ajouter un contrat' in str(response.content) 

        # User enters contract insert page
        contract_url = reverse('contract_insert')
        response = self.client.get(contract_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/contract/'

        # User creates a contract
        self.apartment = self.apartment
        self.occupant = self.occupant
        self.agency = self.user
        self.start_date = date.today()
        contract_duration = self.start_date.year + 3
        self.end_date = self.start_date.replace(contract_duration)
        self.deposit = True

        self.contract = Contract.objects.create(apartment=self.apartment, occupant=self.occupant, agency=self.agency, start_date=self.start_date, end_date=self.end_date, deposit=self.deposit)
        self.contract.save()
    
        # Check if the contract is created with the correct data
        self.assertEqual(self.contract.apartment, self.apartment)
        self.assertEqual(self.contract.occupant, self.occupant)
        self.assertEqual(self.contract.agency, self.agency)
        self.assertEqual(Contract.objects.count(), 1)

    # User creates an itemslist for this contract
        self.contract = self.contract
        self.date = date.today()
        self.list_type = "SORTIE"
        self.comments = "Bon etat global"

        self.itemslist = ItemsList.objects.create(contract=self.contract, date=self.date, list_type=self.list_type, comments=self.comments)
        self.itemslist.save()
    
        # Check if the itemslist is created with the correct data
        self.assertEqual(self.itemslist.contract, self.contract)
        self.assertEqual(self.itemslist.list_type, self.list_type)
        self.assertEqual(ItemsList.objects.count(), 1)

        # Load the itemslist update URL in the "client"
        itemslist_edit_url = reverse("itemslist_update", kwargs={"id": self.itemslist.id})
        response = self.client.get(itemslist_edit_url)
        
        # Check if the form is present in the HTML response 
        # This response should contain occupant and list type
        assert response.status_code == 200
        assert "Jones Tom" in str(response.content)
        assert "Sortie" in str(response.content)
 
        # We send the udpate form via client, only changing the comments
        # everything else will be the same as self.itemslist
        itemslist_data = ItemsListForm(instance=self.itemslist).initial
        itemslist_data["list_type"] = "Entrée"
        
        # Submit the update form
        response = self.client.post(itemslist_edit_url, itemslist_data)

        # After the form is submitted, the client should be redirected 
        self.assertEqual(response.status_code, 302)

        # The end date of the contract should be changed and permanently
        # Doing a new database query for agency's email return the updated end date.
        itemslist = ItemsList.objects.get(id=self.itemslist.id)
        self.assertEqual(itemslist.list_type, "Entrée")    

    def test_user_deletes_itemslist_from_list(self):

        # Check if the user is created and logged in
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.is_authenticated, True) 

        # User enters apartment insert page
        apartment_url = reverse('apartment_insert')
        response = self.client.get(apartment_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/apartment/'

        # User creates an apartment
        self.address = "15 rue de la Republique"
        self.address_complement = "3-2"
        self.city = "Lyon"
        self.postal_code = "69005"
        self.rental_price = 1200.00
        self.charges_price = 400.00
        self.deposit_price = 2400.00

        self.apartment = Apartment.objects.create(address=self.address, address_complement=self.address_complement, city=self.city, postal_code=self.postal_code, rental_price=self.rental_price, charges_price=self.charges_price, deposit_price=self.deposit_price)
        self.apartment.save()
    
        # Check if the apartment is created with the correct data
        self.assertEqual(self.apartment.address, self.address)
        self.assertEqual(Apartment.objects.count(), 1)

        # User enters the occupant insert page
        occupant_url = reverse('occupant_insert')
        response = self.client.get(occupant_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/occupant/'

        # User creates an occupant
        self.first_name = "Tom"
        self.last_name = "Jones"
        self.email = "tom@jones.com"

        self.occupant = Occupant.objects.create(first_name=self.first_name, last_name=self.last_name, email=self.email)
        self.occupant.save()

        # Check if the occupant is created with the correct data
        self.assertEqual(self.occupant.last_name, self.last_name)
        self.assertEqual(Occupant.objects.count(), 1)

        # Load the contract list URL in the "client"
        contractlist_url = reverse('contract_list')
        response = self.client.get(contractlist_url)

        # Check if the page response is 200 & if the path is correct
        # This response should contain "Ajouter un contrat" string, button available only for logged in users 
        assert response.status_code == 200
        assert response.context['request'].path == '/contract/list/'
        assert 'Ajouter un contrat' in str(response.content) 

        # User enters contract insert page
        contract_url = reverse('contract_insert')
        response = self.client.get(contract_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/contract/'

        # User creates a contract
        self.apartment = self.apartment
        self.occupant = self.occupant
        self.agency = self.user
        self.start_date = date.today()
        contract_duration = self.start_date.year + 3
        self.end_date = self.start_date.replace(contract_duration)
        self.deposit = True

        self.contract = Contract.objects.create(apartment=self.apartment, occupant=self.occupant, agency=self.agency, start_date=self.start_date, end_date=self.end_date, deposit=self.deposit)
        self.contract.save()
    
        # Check if the contract is created with the correct data
        self.assertEqual(self.contract.apartment, self.apartment)
        self.assertEqual(self.contract.occupant, self.occupant)
        self.assertEqual(self.contract.agency, self.agency)
        self.assertEqual(Contract.objects.count(), 1)
        
        # User enters itemslist insert page
        itemslist_url = reverse('itemslist_insert')
        response = self.client.get(itemslist_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/itemslist/'

        # User creates an itemslist for this contract
        self.contract = self.contract
        self.date = date.today()
        self.list_type = "SORTIE"
        self.comments = "Bon etat global"

        self.itemslist = ItemsList.objects.create(contract=self.contract, date=self.date, list_type=self.list_type, comments=self.comments)
        self.itemslist.save()
    
        # Check if the itemslist is created with the correct data
        self.assertEqual(self.itemslist.contract, self.contract)
        self.assertEqual(self.itemslist.list_type, self.list_type)
        self.assertEqual(ItemsList.objects.count(), 1)

        # Load the itemslist delete URL in the "client"
        itemslist_delete_url = reverse("itemslist_delete", kwargs={"id": self.itemslist.id})
        response = self.client.get(itemslist_delete_url)

        # Check that the itemslist/delete/id/ leads to a 302 status code to redirect the user to the itemslistlist
        self.assertEqual(response.status_code, 302)

        # Doing a new database query for itemslist's id does not exist anymore
        with self.assertRaises(ItemsList.DoesNotExist): 
            ItemsList.objects.get(id=self.itemslist.id)