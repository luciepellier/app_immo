from django.contrib.auth.views import LoginView

# Create your views here.

class LoginView(LoginView):
    template_name = 'registration/login.html'

