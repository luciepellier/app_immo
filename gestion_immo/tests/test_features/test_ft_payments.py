from django.test import TestCase
from django.urls import reverse
from accounts.models import Agency
from gestion_immo.models import Apartment, Occupant, Contract, Payment
from gestion_immo.forms import PaymentForm
from datetime import date

class PaymentFeatureTest(TestCase):

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

    def create_apartment(self):
        self.address = "15 rue de la Republique"
        self.address_complement = "3-2"
        self.city = "Lyon"
        self.postal_code = "69005"
        self.rental_price = 1200.00
        self.charges_price = 400.00
        self.deposit_price = 2400.00

        self.apartment = Apartment.objects.create(address=self.address, address_complement=self.address_complement, city=self.city, postal_code=self.postal_code, rental_price=self.rental_price, charges_price=self.charges_price, deposit_price=self.deposit_price)
        self.apartment.save()

    def create_occupant(self):
        self.first_name = "Tom"
        self.last_name = "Jones"
        self.email = "tom@jones.com"
        self.occupant = Occupant.objects.create(first_name=self.first_name, last_name=self.last_name, email=self.email)
        self.occupant.save()

    def create_contract(self):
        self.apartment = self.apartment
        self.occupant = self.occupant
        self.agency = self.user
        self.start_date = date.today()
        contract_duration = self.start_date.year + 3
        self.end_date = self.start_date.replace(contract_duration)
        self.deposit = True
        self.contract = Contract.objects.create(apartment=self.apartment, occupant=self.occupant, agency=self.agency, start_date=self.start_date, end_date=self.end_date, deposit=self.deposit)
        self.contract.save()

    def create_payments(self):
        self.contract_1 = self.contract
        self.date_1 = date.today()
        self.source_1 = "Locataire"
        self.rental_1 = 900.00
        self.charges_1 = 200.00
        self.payment_1 = Payment.objects.create(contract=self.contract_1, date=self.date_1, source=self.source_1, rental=self.rental_1, charges=self.charges_1)
        self.payment_1.save()
        
#         self.contract_2 = self.contract
#         self.date_2 = date.today()
#         self.payment_date_2 = self.date_2.month + 1
#         self.date_2 = self.date_2.replace(self.payment_date_2)
#         self.source_2 = "Locataire"
#         self.rental_2 = 900.00
#         self.charges_2 = 200.00
#         self.payment_2 = Payment.objects.create(contract=self.contract_2, date=self.date_2, source=self.source_2, rental=self.rental_2, charges=self.charges_2)
#         self.payment_2.save()
# 
#         self.contract_3 = self.contract
#         self.date_3 = date.today()
#         self.payment_date_3 = self.date_3.month + 2
#         self.date_· = self.date_3.replace(self.payment_date_3)
#         self.source_3 = "CAF"
#         self.rental_3 = 450.00
#         self.charges_3 = 0.00
#         self.payment_3 = Payment.objects.create(contract=self.contract, date=self.date_3, source=self.source_3, rental=self.rental_3, charges=self.charges_3)
#         self.payment_3.save()

    def setUp(self):
        self.create_log_in_agency()
        self.create_apartment()
        self.create_occupant()
        self.create_contract()
        self.create_payments()      

    def test_user_creates_and_edits_payment(self):

        # Check if the user is created and logged in
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.is_authenticated, True) 

        # User enters apartment insert page
        apartment_url = reverse('apartment_insert')
        response = self.client.get(apartment_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/apartment/'
    
        # Check if the apartment is created with the correct data
        self.assertEqual(self.apartment.address, self.address)
        self.assertEqual(Apartment.objects.count(), 1)

        # User enters the occupant insert page
        occupant_url = reverse('occupant_insert')
        response = self.client.get(occupant_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/occupant/'

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
    
        # Check if the contract is created with the correct data
        self.assertEqual(self.contract.apartment, self.apartment)
        self.assertEqual(self.contract.occupant, self.occupant)
        self.assertEqual(self.contract.agency, self.agency)
        self.assertEqual(Contract.objects.count(), 1)

        # User enters payment insert page
        payment_url = reverse('payment_insert')
        response = self.client.get(payment_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/payment/'
    
        # Check if the payment is created with the correct data
        self.assertEqual(self.payment_1.contract, self.contract_1)
        self.assertEqual(self.payment_1.rental, self.rental_1)
        self.assertEqual(Payment.objects.count(), 1)

        # Load the payment update URL in the "client"
        payment_edit_url = reverse("payment_update", kwargs={"id": self.payment_1.id})
        response = self.client.get(payment_edit_url)
        
        # Check if the form is present in the HTML response 
        # This response should contain rental cost and payment source
        assert response.status_code == 200
        assert "900.00" in str(response.content)
        assert "Locataire" in str(response.content)
 
        # We send the udpate form via client, only changing the rental cost
        # everything else will be the same as self.payment
        payment_data = PaymentForm(instance=self.payment_1).initial
        payment_data["rental"] = 1000.00
        
        # Submit the update form
        response = self.client.post(payment_edit_url, payment_data)

        # After the form is submitted, the client should be redirected 
        self.assertEqual(response.status_code, 302)

        # The rental paid should be changed and permanently
        # Doing a new database query for agency's email return the updated rental paid.
        payment = Payment.objects.get(id=self.payment_1.id)
        self.assertEqual(payment.rental, 1000.00)    

    def test_user_deletes_payment_from_list(self):

        # Check if the user is created and logged in
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.is_authenticated, True) 

        # User enters apartment insert page
        apartment_url = reverse('apartment_insert')
        response = self.client.get(apartment_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/apartment/'
    
        # Check if the apartment is created with the correct data
        self.assertEqual(self.apartment.address, self.address)
        self.assertEqual(Apartment.objects.count(), 1)

        # User enters the occupant insert page
        occupant_url = reverse('occupant_insert')
        response = self.client.get(occupant_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/occupant/'

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
    
        # Check if the contract is created with the correct data
        self.assertEqual(self.contract.apartment, self.apartment)
        self.assertEqual(self.contract.occupant, self.occupant)
        self.assertEqual(self.contract.agency, self.agency)
        self.assertEqual(Contract.objects.count(), 1)
        
        # User enters payment insert page
        payment_url = reverse('payment_insert')
        response = self.client.get(payment_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/payment/'
    
        # Check if the payment is created with the correct data
        self.assertEqual(self.payment_1.contract, self.contract_1)
        self.assertEqual(self.payment_1.rental, self.rental_1)
        self.assertEqual(Payment.objects.count(), 1)

        # Load the payment delete URL in the "client"
        payment_delete_url = reverse("payment_delete", kwargs={"id": self.payment_1.id})
        response = self.client.get(payment_delete_url)

        # Check that the payment/delete/id/ leads to a 302 status code to redirect the user to the payment list
        self.assertEqual(response.status_code, 302)

        # Doing a new database query for payment's id does not exist anymore
        with self.assertRaises(Payment.DoesNotExist): 
            Payment.objects.get(id=self.payment_1.id)
