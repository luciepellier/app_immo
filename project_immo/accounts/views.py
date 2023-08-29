from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# class PasswordResetView(generic.CreateView):
#     form_class = PasswordResetForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/password_reset_form.html"