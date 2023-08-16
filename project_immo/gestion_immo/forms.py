from django import forms
from project_immo import settings
from .models import Apartment, Occupant, Contract, ItemsList, Payment, Receipt, Agency

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ('address','address_complement','postal_code','city','rental_price','charges_price','deposit_price')
        labels = {
            'address' : 'Adresse',
            'address_complement' : 'Complément d\'adresse',
            'city' : 'Ville',
            'postal_code' : 'Code postal',
            'rental_price': 'Montant du loyer',
            'charges_price': 'Montant des charges',
            'deposit_price': 'Montant du dépôt de garantie',
        }

    def __init__(self, *args, **kwargs):
        super(ApartmentForm, self).__init__(*args, **kwargs)
        self.fields['address_complement'].required = False

class OccupantForm(forms.ModelForm):

    class Meta:
        model = Occupant
        fields = ('first_name','last_name','email')
        labels = {
            'first_name' : 'Prénom',
            'last_name' : 'Nom',
            'email' : 'E-mail',
        }      

class AgencyForm(forms.ModelForm):

    class Meta:
        model = Agency
        fields = ('name','city','commission')
        labels = {
            'name' : 'Nom',
            'city' : 'Ville',
            'commission' : 'Commission',
        }      

class ContractForm(forms.ModelForm):
    start_date = forms.DateField.input_formats=settings.DATE_INPUT_FORMATS
    end_date = forms.DateField.input_formats=settings.DATE_INPUT_FORMATS

    class Meta:
        model = Contract
        fields = ('apartment','occupant','agency','start_date', 'end_date', 'deposit')
        labels = {
            'apartment' : 'Appartement',
            'occupant' : 'Locataire',
            'agency' : 'Agence',
            'start_date' : 'Date de début',
            'end_date' : 'Date de fin',
            'deposit' : 'Dépôt de garantie',
        }      

    def __init__(self, *args, **kwargs):
        super(ContractForm,self).__init__(*args, **kwargs)
        self.fields['apartment'].empty_label = 'Sélectionner un appartement'
        self.fields['occupant'].empty_label = 'Sélectionner un locataire'
        self.fields['agency'].empty_label = 'Sélectionner une agence'

class ItemsListForm(forms.ModelForm):
    date = forms.DateField.input_formats=settings.DATE_INPUT_FORMATS
    class Meta:
        model = ItemsList
        fields = ('contract','date','list_type', 'comments')
        labels = {
            'contract' : 'Contrat',
            'date' : 'Date',
            'list_type' : 'Type d\'état des lieux',
            'comments' : 'Commentaires',
        }      

    def __init__(self, *args, **kwargs):
        super(ItemsListForm,self).__init__(*args, **kwargs)
        self.fields['contract'].empty_label = 'Sélectionner un contrat'

class PaymentForm(forms.ModelForm):
    date = forms.DateField.input_formats=settings.DATE_INPUT_FORMATS
    class Meta:
        model = Payment
        fields = ('contract','date', 'source', 'rental', 'charges')
        labels = {
            'contract' : 'Contrat',
            'date' : 'Date',
            'source' : 'Source',
            'rental' : 'Montant du Loyer',
            'charges' : 'Montant des Charges',
        }      

    def __init__(self, *args, **kwargs):
        super(PaymentForm,self).__init__(*args, **kwargs)
        self.fields['contract'].empty_label = 'Sélectionner un contrat'

class ReceiptForm(forms.ModelForm):
    start_date = forms.DateField.input_formats=settings.DATE_INPUT_FORMATS
    end_date = forms.DateField.input_formats=settings.DATE_INPUT_FORMATS    
    class Meta:
        model = Receipt
        fields = ('contract', 'start_date', 'end_date')
        labels = {
            'contract' : 'Contrat',
            'start_date' : 'Date de début',
            'end_date' : 'Date de fin',
        }      

    def __init__(self, *args, **kwargs):
        super(ReceiptForm,self).__init__(*args, **kwargs)
        self.fields['contract'].empty_label = 'Sélectionner un contrat'