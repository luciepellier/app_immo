from django.shortcuts import render, redirect
from .forms import ApartmentForm, OccupantForm, ContractForm, ItemsListForm
from .models import Apartment, Occupant, Contract, ItemsList

# Create your views here.

# Apartment views to get a list and add, edit and remove an apartment

def apartment_list(request):
    context = {'apartment_list' : Apartment.objects.all()}
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
    context = {'occupant_list' : Occupant.objects.all()}
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
        # if id is 0 a new occupant is created
        if id == 0:
            form = ItemsListForm(request.POST)
        # otherwise the occupant info is updated
        else:
            itemslist = ItemsList.objects.get(pk=id)
            form = ItemsListForm(request.POST, instance = itemslist) 
        # if the validation is ok then save to db          
        if form.is_valid():
            form.save()
        # redirect to the list to check
        return redirect('/itemslist/list')

def itemslist_delete(request,id):
    itemslist = ItemsList.objects.get(pk=id)
    itemslist.delete()
    return redirect('/itemslist/list')