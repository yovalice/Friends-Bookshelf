from django.shortcuts import render

from users.forms import UserLoginForm
from users.forms import UserRegisterForm

def home_page(request):
    return render(request, 'home.html')
