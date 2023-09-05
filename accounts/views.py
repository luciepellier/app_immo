from django.shortcuts import render

# Create your views here.

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class LoginView(LoginView):
    template_name = 'registration/login.html'

