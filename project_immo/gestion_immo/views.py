from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404 
from django.db.models import Sum
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

from .forms import ApartmentForm, OccupantForm, ContractForm, ItemsListForm, PaymentForm, ReceiptForm, AgencyForm
from .models import Apartment, Occupant, Contract, ItemsList, Payment, Receipt, Agency

from datetime import datetime

# Create your views here.

# Apartment views to get a list and add, edit and remove an apartment

def apartment_list(request):
    context = {'apartment_list' : Apartment.objects.all().order_by('city','postal_code')}
    return render(request, 'apartment_management/apartment_list.html', context)

def apartment_form(request, id=0):
    # manage get request
    if request.method == 'GET':
        if id == 0:
            form = ApartmentForm()
        else:
            #filter by id
            apartment = Apartment.objects.get(pk=id)
            # return the form object
            form = ApartmentForm(instance = apartment)
        return render(request, 'apartment_management/apartment_form.html', {'form':form})
    # manage post request
    else:
        # if id is 0 a new apartment is created
        if id == 0:
            form = ApartmentForm(request.POST)
        # otherwise the apartment info is updated
        else:
            apartment = Apartment.objects.get(pk=id)
            form = ApartmentForm(request.POST, instance = apartment) 
        # if the validation is ok then save to db          
        if form.is_valid():
            form.save()
        # redirect to the list to check
        return redirect('/apartment/list')

def apartment_delete(request,id):
    apartment = Apartment.objects.get(pk=id)
    apartment.delete()
    return redirect('/apartment/list')

# Functions to get a list and add, edit and remove an occupant

def occupant_list(request):
    context = {'occupant_list' : Occupant.objects.all().order_by('last_name')}
    return render(request, 'occupant_management/occupant_list.html', context)

def occupant_form(request, id=0):
    # manage get request
    if request.method == 'GET':
        if id == 0:
            form = OccupantForm()
        else:
            #filter by id
            occupant = Occupant.objects.get(pk=id)
            # return the form object
            form = OccupantForm(instance = occupant)
        return render(request, 'occupant_management/occupant_form.html', {'form':form})
    # manage post request
    else:
        # if id is 0 a new occupant is created
        if id == 0:
            form = OccupantForm(request.POST)
        # otherwise the occupant info is updated
        else:
            occupant = Occupant.objects.get(pk=id)
            form = OccupantForm(request.POST, instance = occupant) 
        # if the validation is ok then save to db          
        if form.is_valid():
            form.save()
        # redirect to the list to check
        return redirect('/occupant/list')

def occupant_delete(request,id):
    occupant = Occupant.objects.get(pk=id)
    occupant.delete()
    return redirect('/occupant/list')

# Functions to get a list and add, edit and remove an Agency

def agency_list(request):
    context = {'agency_list' : Agency.objects.all().order_by('-first_name')}
    return render(request, 'agency_management/agency_list.html', context)

def agency_form(request, id=0):
    # manage get request
    if request.method == 'GET':
        if id == 0:
            form = AgencyForm()
        else:
            #filter by id
            agency = Agency.objects.get(pk=id)
            # return the form object
            form = AgencyForm(instance = agency)
        return render(request, 'agency_management/agency_form.html', {'form':form})
    # manage post request
    else:
        # if id is 0 a new payment is created
        if id == 0:
            form = AgencyForm(request.POST)
        # otherwise the payment info is updated
        else:
            agency = Agency.objects.get(pk=id)
            form = AgencyForm(request.POST, instance = agency) 
        # if the validation is ok then save to db          
        if form.is_valid():
            form.save()
        # redirect to the list to check
        return redirect('/agency/list/')

def agency_delete(request,id):
    agency = Agency.objects.get(pk=id)
    agency.delete()
    return redirect('/agency/list')

# Functions to get a list and add, edit and remove a Contract (linking an Apartment and a Occupant)

def contract_list(request):
    context = {'contract_list' : Contract.objects.all()}
    return render(request, 'contract_management/contract_list.html', context)

def contract_form(request, id=0):
    # manage get request
    if request.method == 'GET':
        if id == 0:
            form = ContractForm()
        else:
            #filter by id
            contract = Contract.objects.get(pk=id)
            # return the form object
            form = ContractForm(instance = contract)
        return render(request, 'contract_management/contract_form.html', {'form':form})
    # manage post request
    else:
        # if id is 0 a new occupant is created
        if id == 0:
            form = ContractForm(request.POST)
        # otherwise the occupant info is updated
        else:
            contract = Contract.objects.get(pk=id)
            form = ContractForm(request.POST, instance = contract) 
        # if the validation is ok then save to db          
        if form.is_valid():
            form.save()
        else:
            return render(request, 'contract_management/contract_form.html', {'form' : form})

        # redirect to the list to check
        return redirect('/contract/list')

def contract_delete(request,id):
    contract = Contract.objects.get(pk=id)
    contract.delete()
    return redirect('/contract/list')

# Functions to get a list and add, edit and remove an ItemsList linked to a Contract

def itemslist_list(request):
    context = {'itemslist_list' : ItemsList.objects.all()}
    return render(request, 'itemslist_management/itemslist_list.html', context)

def itemslist_form(request, id=0):
    # manage get request
    if request.method == 'GET':
        if id == 0:
            form = ItemsListForm()
        else:
            #filter by id
            itemslist = ItemsList.objects.get(pk=id)
            # return the form object
            form = ItemsListForm(instance = itemslist)
        return render(request, 'itemslist_management/itemslist_form.html', {'form':form})
    # manage post request
    else:
        # if id is 0 a new itemlist is created
        if id == 0:
            form = ItemsListForm(request.POST)
        # otherwise the itemlist info is updated
        else:
            itemslist = ItemsList.objects.get(pk=id)
            form = ItemsListForm(request.POST, instance = itemslist, itemslist_pk=id) 
        # if the validation is ok then save to db          
        if form.is_valid():
            form.save()
        else:
            return render(request, 'itemslist_management/itemslist_form.html', {'form' : form})
        # redirect to the list to check
        return redirect('/itemslist/list')

def itemslist_delete(request,id):
    itemslist = ItemsList.objects.get(pk=id)
    itemslist.delete()
    return redirect('/itemslist/list')

# Functions to get a list and add, edit and remove a Payment linked to a Contract

def payment_list(request):
    context = {'payment_list' : Payment.objects.all().order_by('-date','contract')}
    return render(request, 'payment_management/payment_list.html', context)

def payment_form(request, id=0):
    # manage get request
    if request.method == 'GET':
        if id == 0:
            form = PaymentForm()
        else:
            #filter by id
            payment = Payment.objects.get(pk=id)
            # return the form object
            form = PaymentForm(instance = payment)
        return render(request, 'payment_management/payment_form.html', {'form':form})
    # manage post request
    else:
        # if id is 0 a new payment is created
        if id == 0:
            form = PaymentForm(request.POST)
        # otherwise the payment info is updated
        else:
            payment = Payment.objects.get(pk=id)
            form = PaymentForm(request.POST, instance = payment) 
        # if the validation is ok then save to db          
        if form.is_valid():
            form.save()
        # redirect to the list to check
        return redirect('/payment/list')

def payment_delete(request,id):
    payment = Payment.objects.get(pk=id)
    payment.delete()
    return redirect('/payment/list')

# Get List of Total Rental payments by Contract + Total amount

def rental_list(request, id):
    contract_payments = Payment.objects.all().filter(contract__id=id).filter(source__contains="Locataire")
    total_amount = contract_payments.aggregate(sum=Sum('rental')+Sum('charges'))['sum'] or 0.00
    context = {'payment_list' :  contract_payments, 'total_amount': total_amount}
    return render(request, 'payment_management/rental_list.html', context)

def commission_list(request, id):
    contracts = Contract.objects.filter(agency__id=id)
    all_contract_payments = Payment.objects.filter(contract__in=contracts).filter(source__contains="Locataire")
    total_amount = all_contract_payments.aggregate(sum=Sum('rental')+Sum('charges'))['sum'] or 0.00
    total_commission = (total_amount * 8) / 100
    context = {'payment_list' :  all_contract_payments, 'total_commission': total_commission}
    return render(request, 'payment_management/commission_list.html', context)

# Functions to create a form and get a Rental Receipt list for a Contract in a date range

# define the set of months that exists between start date and end date inputs
def months_between_dates(start_date, end_date):
    months = set()
    while start_date <= end_date:
        months.add(
            int(start_date.strftime('%m'))
        )
        if start_date.month == 12:
            start_date = start_date.replace(year=start_date.year + 1, month=1)
        else:
            start_date = start_date.replace(month=start_date.month + 1)
    
    return months

# define the receipt functions

def receipt(request):

    # print(request.POST)

    contract_id = request.POST.get("contract")
    contract = get_object_or_404(Contract, id=contract_id)
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    start_date_obj = datetime.strptime(start_date, "%d-%m-%Y")
    end_date_obj = datetime.strptime(end_date, "%d-%m-%Y")

    # print(start_date_obj)
    # print(end_date_obj)

    contract_payments = Payment.objects.filter(contract__id=contract_id, date__gte=start_date_obj, 
                                               date__lte=end_date_obj).filter(source__contains="Locataire")

    # define the set of months in which payments were completed
    months_in_which_payments_were_done = set()
    for payment in contract_payments:
        payment_date = payment.date
        payment_month = payment_date.month
        months_in_which_payments_were_done.add(payment_month)
    
    print(months_in_which_payments_were_done)

    # define the set of months we generate the receipt for based on months between start and end date
    months_we_generate_receipt_for = months_between_dates(start_date_obj, end_date_obj)
    # print(months_we_generate_receipt_for)

    # compare the two sets of months and determine if all payments are or not completed
    is_payment_complete = False
    if months_in_which_payments_were_done == months_we_generate_receipt_for:
        is_payment_complete = True

    context = {"contract_payments": contract_payments, "is_payment_complete": is_payment_complete, "contract": contract, 
               "start_date": start_date, "end_date": end_date}
    return render(request, 'receipt_management/receipt.html', context)

# Functions to create the Receipt form

def receipt_form(request, id=0):
    # manage get request
    if request.method == 'GET':
        if id == 0:
            form = ReceiptForm()
        else:
            #filter by id
            receipt = Receipt.objects.get(pk=id)
            # return the form object
            form = ReceiptForm(instance = receipt)
        return render(request, 'receipt_management/receipt_form.html', {'form':form})
    # manage post request
    else:
        # if id is 0 a new receipt is created
        if id == 0:
            form = ReceiptForm(request.POST)
        # otherwise the receipt info is updated
        else:
            receipt = Receipt.objects.get(pk=id)
            form = ReceiptForm(request.POST, instance = receipt)
        # if the validation is ok then save to db          
        if form.is_valid():
            form.save()
        # redirect to the list to check
        return redirect('/receipt/')
    
def render_pdf_view(request):

    template_path = os.path.join(
        settings.BASE_DIR,
        "gestion_immo",
        "templates",
        "receipt_management",
        "receipt.html"
    )
    
    template = get_template(template_path)

    contract_id = request.POST.get("contract")
    contract = get_object_or_404(Contract, id=contract_id)
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = start_date_obj.strftime("%d-%m-%Y")
    end_date = end_date_obj.strftime("%d-%m-%Y")

    contract_payments = Payment.objects.filter(contract=contract, date__gte=start_date_obj, 
                                               date__lte=end_date_obj).filter(source__contains="Locataire")
    
    months_in_which_payments_were_done = set()
    for payment in contract_payments:
        payment_date = payment.date
        payment_month = payment_date.month
        months_in_which_payments_were_done.add(payment_month)

    months_we_generate_receipt_for = months_between_dates(start_date_obj, end_date_obj)

    is_payment_complete = ( months_in_which_payments_were_done == months_we_generate_receipt_for )

    context = {'contract': contract, 'contract_payments': contract_payments, 'is_payment_complete': is_payment_complete, 
                'start_date': start_date, 'end_date': end_date}


    if not is_payment_complete:
        return render(request, 'receipt_management/no-receipt.html', context)

    html = template.render(context)
    result = BytesIO()
    pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    return HttpResponse(result.getvalue(), content_type="application/pdf")
