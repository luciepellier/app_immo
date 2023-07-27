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
    # get and post requests to add an occupant
    path('occupant/', views.occupant_form, name='occupant_insert'),
    # get and post requests to edit an occupant
    path('occupant/<int:id>/', views.occupant_form, name='occupant_update'),
    # delete an occupant
    path('occupant/delete/<int:id>/', views.occupant_delete, name='occupant_delete'),    
    # get request to get & display all the occupant in a list
    path('occupant/list/', views.occupant_list, name='occupant_list'),
    # contracts paths
    path('contract/', views.contract_form, name='contract_insert'),
    # get and post requests to edit an occupant
    path('contract/<int:id>/', views.contract_form, name='contract_update'),
    # delete an occupant
    path('contract/delete/<int:id>/', views.contract_delete, name='contract_delete'),    
    # get request to get & display all the occupant in a list
    path('contract/list/', views.contract_list, name='contract_list'),    
]