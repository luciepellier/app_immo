from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Agency

class UserAuth(TestCase):
    def setUp(self):
        self.username = "johnsmith"
        self.password = "smith_123098"
        self.email = "john@smith.com"
        self.first_name = "John"
        self.last_name = "Smith"

        self.user = Agency.objects.create(username=self.username, email=self.email, first_name=self.first_name, last_name=self.last_name)
        self.user.set_password(self.password)
        self.user.save()

    def test_user_creates_account_and_logs_in(self):
        c = Client()
        c.force_login(self.user)
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.is_authenticated, True)
        contractlist_url = reverse('contract_list')
        response = c.get(contractlist_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/contract/list/'
        assert 'Ajouter un contrat' in str(response.content) 
            
    def test_user_edits_and_save_info(self):
        c = Client()
        c.force_login(self.user)

        agency_edit_url = reverse('agency_update', kwargs={'id': self.user.id})
        response = c.get(agency_edit_url)
        
        assert self.username in str(response.content)
        assert self.email in str(response.content)

        # update the email
        # 'username', 'first_name', 'last_name', 'email', 'city'
        payload = {
            "username": self.user.username,
            "email": "luciepellier@gmail.com",
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "city": self.user.city
        }
        
        response = c.post(agency_edit_url, payload)

        print("the path of the request is: ", response.context['request'].path)

        print(response.content)

        assert response.status_code == 200
        assert response.context['request'].path == 'agency/<int:id>/'







        

