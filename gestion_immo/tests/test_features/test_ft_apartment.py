from django.test import TestCase
from django.urls import reverse
from accounts.models import Agency
from gestion_immo.models import Apartment
from gestion_immo.forms import ApartmentForm

class ApartementFeatureTest(TestCase):
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

    def test_user_creates_and_edits_apartment(self):

        # Check if the user is created and logged in
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.is_authenticated, True) 

        # Load the apartment list URL in the "client"
        apartmentlist_url = reverse('apartment_list')
        response = self.client.get(apartmentlist_url)
        # Check if the page response is 200 & if the path is correct
        # This response should contain "Ajouter un appartment" string, button available only for logged in users
        assert response.status_code == 200
        assert response.context['request'].path == '/apartment/list/'
        assert 'Ajouter un appartement' in str(response.content) 

        # User creates an apartment
        self.address = "15 rue de la République"
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

        # Load the apartment update URL in the "client"
        apartment_edit_url = reverse("apartment_update", kwargs={"id": self.apartment.id})
        response = self.client.get(apartment_edit_url)
        
        # Check if the form is present in the HTML response 
        # This response should contain address and city
        assert response.status_code == 200
        assert 'Enregistrer' in str(response.content)
        assert 'Montant des charges' in str(response.content)
        assert "Ajouter / Modifier un Appartement" in str(response.content)
        assert self.apartment.address in str(response.content)
        assert self.city in str(response.content)
 
#         # We send the udpate form via client, only changing the charges price 
#         # everything else will be the same as self.apartment
#         apartment_data = ApartmentForm(instance=self.apartment).initial
#         apartment_data["charges_price"] = 200.00
#         
#         # Submit the update form
#         response = self.client.post(apartment_edit_url, apartment_data)
# 
#         # After the form is submitted, the client should be redirected to Apartment list page
#         self.assertRedirects(response, f"/apartment/list/")
# 
#         # The email of the agency should be changed and permanently
#         # Doing a new database query for agency's email return the updated email.
#         apartment = Apartment.objects.get(id=self.apartment.id)
#         self.assertEqual(apartment.charges_price, 200.00)
# 
#     def test_user_deletes_apartment_from_list(self):
#         # Check if the user is created and logged in
#         self.assertEqual(self.user.username, self.username)
#         self.assertEqual(self.user.is_authenticated, True) 
# 
#         # Check if the apartment is created
#         self.assertEqual(self.apartment.address, self.address)
#         self.assertEqual(Apartment.objects.count(), 1)
# 
#         # Load the apartment delete URL in the "client"
#         apartment_delete_url = reverse("apartment_delete", kwargs={"id": self.apartment.id})
#         response = self.client.get(apartment_delete_url)
# 
#         # Check that the apartment/delete/id/ leads to a 302 status code
#         self.assertEqual(response.status_code, 302)
# 
#         # Doing a new database query for apartment's id does not exist anymore
#         with self.assertRaises(Apartment.DoesNotExist): 
#             Apartment.objects.get(id=self.apartment.id)
# 
#     #     # After the apartment is deleted, the client is redirected to apartment list page  
#     #     assert response.status_code == 301 or 302