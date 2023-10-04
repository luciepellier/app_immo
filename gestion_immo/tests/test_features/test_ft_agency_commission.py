from django.test import TestCase
from django.urls import reverse
from accounts.models import Agency
from gestion_immo.models import Apartment, Occupant, Contract, Payment
from datetime import date

class CommissionFeatureTest(TestCase):
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

    def test_user_displays_payments_and_commission_amount(self):

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

        # User enters contract insert page
        payment_url = reverse('payment_insert')
        response = self.client.get(payment_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/payment/'

        # User creates an payment 1 for this contract
        self.contract = self.contract
        self.date = date.today()
        self.source = "Locataire"
        self.rental = 900.00
        self.charges = 200.00

        self.payment_1 = Payment.objects.create(contract=self.contract, date=self.date, source=self.source, rental=self.rental, charges=self.charges)
        self.payment_1.save()
    
        # Check if the payment 1 is created with the correct data
        self.assertEqual(self.payment_1.contract, self.contract)
        self.assertEqual(self.payment_1.rental, self.rental)
        self.assertEqual(Payment.objects.count(), 1)

        # User creates payment 2 for this contract
        self.contract = self.contract
        self.date = date.today()
        new_payment_date = self.date.month + 1
        self.date = self.date.replace(new_payment_date)
        self.source = "Locataire"
        self.rental = 900.00
        self.charges = 200.00

        self.payment_2 = Payment.objects.create(contract=self.contract, date=self.date, source=self.source, rental=self.rental, charges=self.charges)
        self.payment_2.save()

        # Check if the payment 2 is created with the correct data
        self.assertEqual(self.payment_2.contract, self.contract)
        self.assertEqual(self.payment_2.rental, self.rental)
        self.assertEqual(Payment.objects.count(), 2)

        # User creates payment 3 for this contract
        self.contract = self.contract
        self.date = date.today()
        new_payment_date = self.date.month + 2
        self.date = self.date.replace(new_payment_date)
        self.source = "CAF"
        self.rental = 450.00
        self.charges = 0.00

        self.payment_3 = Payment.objects.create(contract=self.contract, date=self.date, source=self.source, rental=self.rental, charges=self.charges)
        self.payment_3.save()

        # Check if the payment 3 is created with the correct data
        self.assertEqual(self.payment_3.contract, self.contract)
        self.assertEqual(self.payment_3.rental, self.rental)
        self.assertEqual(Payment.objects.count(), 3)

        # User enters agency list page
        agency_list_url = reverse('agency_list')
        response = self.client.get(agency_list_url)
        assert response.status_code == 200
        assert response.context['request'].path == '/agency/list/'

        # Load the commission list URL in the "client"
        commission_list_url = reverse("commission_list", kwargs={"id": self.user.id})
        response = self.client.get(commission_list_url)
        
        # Check if the page response is 200 & if the path is correct
        # This response should contain "TOTAL COMMISSION" & "176.00" string = total commission
        # This response should contain the occupant and appartment of the contract in the string

        assert response.status_code == 200
        assert 'TOTAL COMMISSION' in str(response.content) 
        assert '176.00' in str(response.content) 
        assert 'Jones Tom' in str(response.content) 
        assert '15 rue de la Republique' in str(response.content) 