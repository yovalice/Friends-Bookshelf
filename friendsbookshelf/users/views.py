from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from pure_pagination.mixins import PaginationMixin

from .forms import UserLoginForm
from .forms import UserRegisterForm
from .forms import UserForgotForm
from .forms import UserConfirmationPasswordForm
from .forms import UserInformationForm
from .models import User, FriendList
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
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                data = {'form': form}
                messages.error(request, 'Looks like the username or email with the information provided already exists.')
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
                # messages.add_message(request, messages.SUCCESS, 'Looks like that username does not exists or the password is incorrect.')
                return HttpResponseRedirect('/')
            else:
                data = {'form': form}
                messages.error(request, 'Looks like that username does not exists or the password is incorrect.')
                print('hey')

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


class EditUserInformation(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserInformationForm
    template_name = 'users/edit_user_information.html'
    # fields = ['first_name', 'last_name', 'bio', 'genter', 'image']
    success_message = ("The User Information was updated successfully.")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditUserInformation, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('user_information', kwargs={'pk': self.request.user.pk})


@login_required
def user_details(request, id):
    user = User.objects.get(id=id)

    friend = FriendList.objects.filter(friend=id, user=request.user)

    posts = Post.objects.select_related('book').prefetch_related(
        'comments').filter(user=user)[:6]

    books_read = BooksRead.objects.filter(user=user)[:6]

    data = {'user_detail': user, 'books_read': books_read,
            'posts': posts, 'friend_accepted': friend.filter(accept=True).exists(),
            'friend_request': friend.filter(accept=False).exists()}

    return render(request, 'users/user_details.html', data)


@login_required
def users_friends_post(request, user_id):
    user_friend = FriendList.objects.select_related(
        'friend', 'user').filter(user=request.user, friend__id=user_id)

    print('woot')

    if user_friend.exists():
        if user_friend.filter(accept=True).exists():
            user_friend = user_friend.first()
            messages.success(request, ('%s %s was deleted from your friend list.') % (user_friend.friend.first_name, user_friend.friend.last_name))
        else:
            user_friend = user_friend.first()
            messages.success(request, ('%s %s friend request was cancelled.') % (user_friend.friend.first_name, user_friend.friend.last_name))         
        
        user_friend.delete()
        print('delete')
    else:
        print('added')
        user_friend = FriendList.objects.create(user=request.user, friend_id=user_id)
        messages.success(request, ('A friend request to %s %s was sent successfully.') % (user_friend.friend.first_name, user_friend.friend.last_name))

    return redirect('user_details', id=user_id)


class Friends(PaginationMixin, ListView):
    paginate_by = 12
    template_name = 'users/friends.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        friends = FriendList.objects.select_related('friend').filter(user=self.request.user)
        return friends
