from django.test import TestCase
from django.urls import reverse
from accounts.models import Agency
from gestion_immo.models import Apartment, Occupant, Contract, Payment
from datetime import date

class ReceiptFeatureTest(TestCase):

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
        self.contract = self.contract
        self.date = date.today()
        self.source = "Locataire"
        self.rental = 900.00
        self.charges = 200.00
        self.payment_1 = Payment.objects.create(contract=self.contract, date=self.date, source=self.source, rental=self.rental, charges=self.charges)
        self.payment_1.save()
        
        self.contract = self.contract
        self.date = date.today()
        self.payment_date_2 = self.date.month + 1
        self.date = self.date.replace(self.payment_date_2)
        self.source = "Locataire"
        self.rental = 900.00
        self.charges = 200.00
        self.payment_2 = Payment.objects.create(contract=self.contract, date=self.date, source=self.source, rental=self.rental, charges=self.charges)
        self.payment_2.save()

        self.contract = self.contract
        self.date = date.today()
        self.payment_date_3 = self.date.month + 2
        self.date = self.date.replace(self.payment_date_3)
        self.source = "CAF"
        self.rental = 450.00
        self.charges = 0.00
        self.payment_3 = Payment.objects.create(contract=self.contract, date=self.date, source=self.source, rental=self.rental, charges=self.charges)
        self.payment_3.save()

    def setUp(self):
        self.create_log_in_agency()
        self.create_apartment()
        self.create_occupant()
        self.create_contract()
        self.create_payments()

    def test_generate_receipt_pdf(self):
        # Ensure the user is logged in
        self.assertTrue(self.user.is_authenticated)

        # User enters the receipt form
        receipt_form_url = reverse('receipt_form')
        response = self.client.get(receipt_form_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'receipt_management/receipt_form.html')

        # Post data to generate a receipt PDF for a date range with satisfied payments
        render_pdf_url = reverse("render_pdf_view")
        data = {
            "contract": self.contract.id,
            "start_date": "2023-10-01",
            "end_date": "2023-10-30",
        }
        response = self.client.post(render_pdf_url, data)
        
        # Check if a PDF is generated for satisfied payments period
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

        # Modify the payments to simulate unsatisfied payments period
        render_pdf_url = reverse("render_pdf_view")
        data = {
            "contract": self.contract.id,
            "start_date": "2023-10-01",
            "end_date": "2023-12-31",
        }

        # Post data to generate a receipt PDF for the same date range with unsatisfied payments
        response = self.client.post(render_pdf_url, data)
        
        # Check if the view redirects to the receipt template for unsatisfied payments
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'receipt_management/no-receipt.html')