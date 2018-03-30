from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from django.core.mail import send_mail

from .forms import UserLoginForm
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form_login = UserLoginForm(request.POST)
        form_register = UserRegisterForm(request.POST)
        if form_login.is_valid():
            userObj = form_login.cleaned_data
            username = userObj['username']
            password = userObj['password']
            if User.objects.filter(username=username).exists() or User.objects.filter(email=username).exists():
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                data = {'form_login': form_login,
                        'form_register': form_register,
                        'error_message': 'Looks like that username does not exists or the password is incorrect.'}

                return render(request, 'register.html', data)

        elif form_register.is_valid():
            userObj = form_register.cleaned_data
            first_name = userObj['first_name']
            last_name = userObj['last_name']
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                data = {'form_login': form_login,
                        'form_register': form_register,
                        'error_message': 'Looks like a username with that email or password already exists.'}
                return render(request, 'register.html', data)
    else:
        form_login = UserLoginForm()
        form_register = UserRegisterForm()

    return render(request, 'register.html', {'form_login': form_login, 'form_register': form_register})


def forgot(request):
    if request.method == 'POST':
        form_forgot = UserForgotForm(request.POST)
        if form_forgot.is_valid():
            subject = 'Reset Password'
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return render(request, 'register.html', {'form_forgot': form_forgot})
        else:
            form_forgot = UserForgotForm(request.POST)
    return render(request, 'register.html', {'form_forgot': form_forgot})


def confirm_password(request):
    if request.method == 'POST':
        form_forgot = UserConfirmForm(request.POST)
        if form_register.is_valid():
            password1 = form.cleaned_data['subject']
            password2 = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/')
        else:
            form_login = UserLoginForm(request.POST)
            form_register = UserRegisterForm(request.POST)
    return render(request, 'register.html', {'form_login': form_login})
