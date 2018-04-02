from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django import forms
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm
from .forms import UserRegisterForm
from .forms import UserForgotForm
from .forms import UserConfirmationPasswordForm
from .forms import UserInformationForm
from .models import User
from books.models import BooksRead, BookWish
from main_app.models import Post


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            first_name = userObj['first_name']
            last_name = userObj['last_name']
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists()):
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                data = {'form': form,
                        'register_error_message': 'Looks like the username or email with the information provided already exists.'}
                return render(request, 'users/register.html', data)
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            password = userObj['password']
            if User.objects.filter(username=username).exists() or User.objects.filter(email=username).exists():
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                data = {'form': form,
                        'login_error_message': 'Looks like that username does not exists or the password is incorrect.'}

                return render(request, 'users/login.html', data)
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def forgot(request):
    if request.method == 'POST':
        form = UserForgotForm(request.POST)
        if form.is_valid():
            subject = 'Reset Password'
            message = ''
            sender = form.cleaned_data['email']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return render(request, 'users/forgot.html', {'form': form})
    else:
        form = UserForgotForm()

    return render(request, 'users/forgot.html', {'form': form})


def confirm_password(request):
    if request.method == 'POST':
        form = UserConfirmationPasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            return render(request, 'users/confirm.html', {'form': form})
    else:
        form = UserConfirmationPasswordForm()
    return render(request, 'users/confirm.html', {'form': form})


@login_required
def edit_user_information(request):
    if request.method == 'POST':
        form = UserInformationForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            return render(request, 'users/edit_user_information.html', {'form': form})
    else:
        form = UserInformationForm()

    return render(request, 'users/edit_user_information.html', {'form': form})


@login_required
def user_details(request, id):
    user = User.objects.get(id=id)

    books_read = BooksRead.objects.filter(user=user)[:10]

    posts = Post.objects.filter(user=user)[:8]

    data = {'user': user, 'books_read': books_read,
            'posts': posts}

    return render(request, 'users/user_details.html', data)