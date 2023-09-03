import datetime
from django import forms
from project_immo import settings
from .models import Apartment, Occupant, Contract, ItemsList, Payment, Receipt
from accounts.models import Agency


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
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Agency
        fields = ('first_name', 'last_name', 'city', 'username', 'password')
        labels = {
            'name' : 'Nom',
            'city' : 'Ville',
        }

    def save(self, commit: bool = ...):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user   

class DateInput(forms.DateInput):
    input_type = 'date'
    
class ContractForm(forms.ModelForm):
    start_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, label='Date de début', help_text='JJ-MM-AAAA', required=True, initial=datetime.date.today)
    end_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, label='Date de fin', help_text='JJ-MM-AAAA', required=False)
    deposit = forms.BooleanField(label='Le dépôt de garantie a-t-il été versé ? (obligatoire)',required=True)

    class Meta:
        model = Contract
        fields = ('apartment','occupant','agency','start_date', 'end_date', 'deposit')
        labels = {
            'apartment' : 'Appartement',
            'occupant' : 'Locataire',
            'agency' : 'Agence',
        }      
        error_messages = {
            'apartment': {
                'unique': 'Un contrat existe déjà pour cet appartement. Veuillez choisir ou entrer un autre appartement.',
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        #if start_date is None:
        #    raise forms.ValidationError("start_date is not supplied with form.. maybe you put on a wrong date format??")

        if (end_date is not None and end_date <= start_date):
            self.add_error('end_date', 'La date de fin ne peut pas être égale ou antérieure à la date de début de contrat.')
            raise forms.ValidationError('Veuillez modifier les dates du contrat.')
        
        # apartment = cleaned_data.get('apartment')
        # contract_already_exists = Contract.objects.filter(apartment=apartment).exists()
        # if contract_already_exists:
        #     self.add_error('apartment', 'Un contrat existe déjà pour cet appartement.')
        #     raise forms.ValidationError('Veuillez choisir ou entrer un autre appartement.')

    def __init__(self, *args, **kwargs):
        super(ContractForm,self).__init__(*args, **kwargs)
        self.fields['apartment'].empty_label = 'Sélectionner un appartement'
        self.fields['occupant'].empty_label = 'Sélectionner un locataire'
        self.fields['agency'].empty_label = 'Sélectionner une agence'

class ItemsListForm(forms.ModelForm):
    date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, label='Date', help_text='JJ-MM-AAAA', required=True, initial=datetime.date.today)
    
    class Meta:
        model = ItemsList
        fields = ('contract','date','list_type', 'comments')
        labels = {
            'contract' : 'Contrat',
            'list_type' : 'Type d\'état des lieux',
            'comments' : 'Commentaires',
        }      

    def clean(self):
        cleaned_data = super().clean()
        contract = cleaned_data.get("contract")
        list_type = cleaned_data.get("list_type")
        itemslist_already_exists = ItemsList.objects.filter(contract=contract, list_type=list_type).exclude(pk=self.itemslist_pk).exists()
        if itemslist_already_exists:
            self.add_error('list_type', (f'L\'état des lieux de type: "{list_type}" existe déjà pour ce contrat.'))
            raise forms.ValidationError('Veuillez modifier le contrat ou type d\'état des lieux.')     

    def __init__(self, *args, **kwargs):
        self.itemslist_pk = None
        if "itemslist_pk" in kwargs:
            self.itemslist_pk = kwargs.pop("itemslist_pk")
        super(ItemsListForm,self).__init__(*args, **kwargs)
        self.fields['contract'].empty_label = 'Sélectionner un contrat'

class PaymentForm(forms.ModelForm):
    date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, label='Date', help_text='JJ-MM-AAAA', required=True, initial=datetime.date.today)
    rental = forms.DecimalField(min_value=100, decimal_places=2, initial=0, required=True, label='Montant du Loyer')
    charges = forms.DecimalField(max_digits=4, decimal_places=2, initial=0, required=False, label='Montant des Charges')
    class Meta:
        model = Payment
        fields = ('contract','date', 'source', 'rental', 'charges')
        labels = {
            'contract' : 'Contrat',
            'source' : 'Source',
        }

    def __init__(self, *args, **kwargs):
        super(PaymentForm,self).__init__(*args, **kwargs)
        self.fields['contract'].empty_label = 'Sélectionner un contrat'

class ReceiptForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput(format = '%d-%m-%Y'), label='Date de début', input_formats=settings.DATE_INPUT_FORMATS)
    end_date = forms.DateField(widget=DateInput(format = '%d-%m-%Y'), label='Date de fin', input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Receipt
        fields = ('contract', 'start_date', 'end_date')
        labels = {
            'contract' : 'Contrat',
        }      

    def __init__(self, *args, **kwargs):
        super(ReceiptForm,self).__init__(*args, **kwargs)
        self.fields['contract'].empty_label = 'Sélectionner un contrat'