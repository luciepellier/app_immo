from django.shortcuts import render, redirect
from .forms import ApartmentForm
from .models import Apartment

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