from django.urls import path, include
from . import views

urlpatterns = [
    # get and post requests to add an apartment
    path('apartment/', views.apartment_form, name='apartment_insert'),
    # get and post requests to edit an apartment
    path('apartment/<int:id>/', views.apartment_form, name='apartment_update'),
    # delete an apartment
    path('apartment/delete/<int:id>/', views.apartment_delete, name='apartment_delete'),    
    # get request to get & display all the apartments in a list
    path('apartment/list/', views.apartment_list, name='apartment_list'),
    # routes for occupant
    path('occupant/', views.occupant_form, name='occupant_insert'),
    path('occupant/<int:id>/', views.occupant_form, name='occupant_update'),
    path('occupant/delete/<int:id>/', views.occupant_delete, name='occupant_delete'),    
    path('occupant/list/', views.occupant_list, name='occupant_list'),
    # routes for contracts 
    path('contract/', views.contract_form, name='contract_insert'),
    path('contract/<int:id>/', views.contract_form, name='contract_update'),
    path('contract/delete/<int:id>/', views.contract_delete, name='contract_delete'),    
    path('contract/list/', views.contract_list, name='contract_list'),    
    # routes for items list
    path('itemslist/', views.itemslist_form, name='itemslist_insert'),
    path('itemslist/<int:id>/', views.itemslist_form, name='itemslist_update'),
    path('itemslist/delete/<int:id>/', views.itemslist_delete, name='itemslist_delete'),    
    path('itemslist/list/', views.itemslist_list, name='itemslist_list'),
    # routes for payment
    path('payment/', views.payment_form, name='payment_insert'),
    path('payment/<int:id>/', views.payment_form, name='payment_update'),
    path('payment/delete/<int:id>/', views.payment_delete, name='payment_delete'),    
    path('payment/list/', views.payment_list, name='payment_list'),
    path('rental/<int:id>/', views.rental_list, name='rental_list'),
    path('commission/<int:id>/', views.commission_list, name='commission_list'),
    # routes for rental receipt
    path('receipt/form/', views.receipt_form, name='receipt_form'),
    path('receipt/', views.receipt, name='receipt'),
    # routes for agency 
    path('agency/', views.agency_form, name='agency_insert'),
    path('agency/<int:id>/', views.agency_form, name='agency_update'),
    path('agency/delete/<int:id>/', views.agency_delete, name='agency_delete'),    
    path('agency/list/', views.agency_list, name='agency_list'),
]