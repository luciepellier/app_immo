from django.urls import path, include
from . import views

urlpatterns = [
    # get and post requests to add an apartment
    path('', views.apartment_form, name='apartment_insert'),
    # get and post requests to edit an apartment
    path('<int:id>/', views.apartment_form, name='apartment_update'),
    # delete an apartment
    path('delete/<int:id>/', views.apartment_delete, name='apartment_delete'),    
    # get request to get & display all the apartments in a list
    path('list/', views.apartment_list, name='apartment_list'),
]