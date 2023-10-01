from django.test import TestCase
from django.urls import reverse
from accounts.models import Agency
from gestion_immo.forms import AgencyUpdateForm

class UserAuth(TestCase):

    def test_user_creates_account_and_logs_in(self):
        # User creates an account
        self.username = "johnsmith"
        self.password = "smith_123098"
        self.email = "john@smith.com"
        self.first_name = "John"
        self.last_name = "Smith"
        self.city = "Madrid"

        self.user = Agency.objects.create(username=self.username, email=self.email, first_name=self.first_name, last_name=self.last_name, city=self.city)
        self.user.set_password(self.password)
        self.user.save()

        # Logs in with the user data
        self.client.force_login(self.user)

        # Check if the user data matches and if user is logged in
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.is_authenticated, True)

        # Load the contract list URL in the "client"
        contractlist_url = reverse('contract_list')
        response = self.client.get(contractlist_url)

        # Check if the page response is 200 & if the path is correct
        # This response should contain "Ajouter un contrat" string, button available only for logged in users 
        assert response.status_code == 200
        assert response.context['request'].path == '/contract/list/'
        assert 'Ajouter un contrat' in str(response.content) 
            
    def test_user_edits_and_save_info(self):
        # User creates an account
        self.username = "johnsmith"
        self.password = "smith_123098"
        self.email = "john@smith.com"
        self.first_name = "John"
        self.last_name = "Smith"
        self.city = "Madrid"
        self.user = Agency.objects.create(username=self.username, email=self.email, first_name=self.first_name, last_name=self.last_name, city=self.city)
        self.user.set_password(self.password)
        self.user.save()

        # Logs in with the user data
        self.client.force_login(self.user)

        # Load the agency update URL in the "client"
        agency_edit_url = reverse("agency_update", kwargs={"id": self.user.id})
        response = self.client.get(agency_edit_url)
        
        # Check if the form is present in the HTML response. 
        # This response should contain username and email
        assert self.username in str(response.content)
        assert self.email in str(response.content)

        # We send the udpate form via client, only changing the email
        # everything else will be the same as self.user
        agency_data = AgencyUpdateForm(instance=self.user).initial
        agency_data["email"] = "johnsmith333@gmail.com"
        
        # Submit the update form
        response = self.client.post(agency_edit_url, agency_data)

        # After the form is submitted, the client should be redirected to Agency list page
        self.assertRedirects(response, f"/agency/list/")

        # The email of the agency should be changed and permanently
        # Doing a new database query for agency's email return the updated email.
        agency = Agency.objects.get(id=self.user.id)
        self.assertEqual(agency.email, "johnsmith333@gmail.com")

    def test_superuser_deletes_account(self):
        # User creates an account
        self.username = "johnsmith"
        self.password = "smith_123098"
        self.email = "john@smith.com"
        self.first_name = "John"
        self.last_name = "Smith"
        self.city = "Madrid"
        self.user = Agency.objects.create(username=self.username, email=self.email, first_name=self.first_name, last_name=self.last_name, city=self.city)
        self.user.set_password(self.password)
        self.user.is_superuser = True
        self.user.save()

        # Logs in with the user data
        self.client.force_login(self.user)

        # Load the agency delete URL in the "client"
        agency_delete_url = reverse("agency_delete", kwargs={"id": self.user.id})
        response = self.client.get(agency_delete_url)

        # Check that the agency/delete/id/ leads to a 302 status code as in Unit tests
        self.assertEqual(response.status_code, 302)

        # Doing a new database query for agency's id does not exist anymore
        with self.assertRaises(Agency.DoesNotExist): 
            Agency.objects.get(id=self.user.id)

        # After the user is deleted, the client is redirected to Agency list page  
        assert response.status_code == 301 or 302
        
        