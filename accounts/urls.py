from django.urls import path
from .views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('password_change', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]