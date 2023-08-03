from django import forms
from .models import Apartment, Occupant, Contract, ItemsList, Payment

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

class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = ('apartment','occupant','start_date', 'end_date')
        labels = {
            'apartment' : 'Appartement',
            'occupant' : 'Locataire',
            'start_date' : 'Date de début',
            'end_date' : 'Date de fin',
        }      

    def __init__(self, *args, **kwargs):
        super(ContractForm,self).__init__(*args, **kwargs)
        self.fields['apartment'].empty_label = 'Sélectionner un appartement'
        self.fields['occupant'].empty_label = 'Sélectionner un locataire'

class ItemsListForm(forms.ModelForm):

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

    class Meta:
        model = Payment
        fields = ('contract','date','payment_type', 'payment_source', 'price')
        labels = {
            'contract' : 'Contrat',
            'date' : 'Date',
            'payment_type' : 'Type de paiement',
            'payment_source' : 'Source',
            'price' : 'Montant',
        }      

    def __init__(self, *args, **kwargs):
        super(PaymentForm,self).__init__(*args, **kwargs)
        self.fields['contract'].empty_label = 'Sélectionner un contrat'