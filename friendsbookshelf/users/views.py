from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.template.loader import render_to_string

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
            user = User.objects.filter(Q(username=username) | Q(email=username))
            if user.exists():
                auth_login(request, user.first())
                return HttpResponseRedirect('/')
            else:
                data = {'form': form}
                messages.error(request, 'Looks like that username does not exists or the password is incorrect.')

                return render(request, 'users/login.html', data)
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def forgot(request):
    if request.method == 'POST':
        form = UserForgotForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
            except User.DoesNotExist:
                messages.error(request, 'The user with that email address does not exist.')
                return HttpResponseRedirect('/forgot/')
 
            uid = user.pk
            token = default_token_generator.make_token(user)

            if settings.DEBUG:
                link = 'http://127.0.0.1:8000/user_reset_password/%s/%s/' % (uid, token)
            else:
                link = 'http://friendsbooksshelf.com/user_reset_password/%s/%s/' % (uid, token)

            text_content = 'Text'
            html_content = render_to_string(
                'users/password_reset_email.html',
                {'link': link}
            )

            msg = EmailMultiAlternatives(subject='Password Reset',
                               from_email='no-reply@friendsbooksshelf.com', to=[form.cleaned_data['email']])
            msg.attach_alternative(html_content, "text/html")
            msg.use_template_subject = True
            msg.use_template_from = True
            msg.send()
            messages.success(request, 'An email to reset your password was sent to ' + form.cleaned_data['email'] + ' email address.')
        return HttpResponseRedirect('/forgot/')
    else:
        form = UserForgotForm()

    return render(request, 'users/forgot.html', {'form': form})


def user_reset_password(request, uid, token):
    if request.method == 'POST':
        form = UserConfirmationPasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 != password2:
                messages.error(request, 'The Password and Confirm Password are not the same.')
                return HttpResponseRedirect('/user_reset_password/' + uid + '/' + token + '/')

            if not uid or not token:
                messages.error(request, 'The token to change your password is invalid.')
                return HttpResponseRedirect('/')

            user_pk = uid
            user = User.objects.get(pk=user_pk)

            if user is not None and default_token_generator.check_token(user, token):
                user.password = make_password(password2)
                user.save()
                messages.success(request, 'The password for your user was successfully changed.')
                return HttpResponseRedirect('/user_reset_password/' + uid + '/' + token + '/')
            else:
                messages.error(request, 'The token to change your password is invalid.')
                return HttpResponseRedirect('/user_reset_password/' + uid + '/' + token + '/')
        else:
            return HttpResponseRedirect('/user_reset_password/' + uid + '/' + token + '/')
    else:
        form = UserConfirmationPasswordForm()

    return render(request, 'users/user_reset_password.html', {'form': form, 'uid': uid, 'token': token})


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
        return reverse_lazy('user_information')


@login_required
def user_details(request, id):
    user = User.objects.get(id=id)

    friend_request_from_user = FriendList.objects.filter(
        user_id=user, friend=request.user)

    if friend_request_from_user.filter(accept=True).exists():
        friend_request_from_user_accept = 'friend_request_from_user'
    elif friend_request_from_user.exists():
        friend_request_from_user_accept = 'friend_request_not_accepted_from_user'
    else:
        friend_request_from_user_accept = None

    friend = FriendList.objects.filter(friend=id, user=request.user)

    posts = Post.objects.select_related('book', 'user', 'book__book',).filter(user=user).order_by('-id')[:6]

    books_read = BooksRead.objects.select_related('book').filter(user=user).order_by('-id')[:6]

    data = {'user_detail': user, 'books_read': books_read,
            'posts': posts, 'friend_accepted': friend.filter(accept=True).exists(),
            'friend_request': friend.filter(accept=False).exists(),
            'friend_request_from_user_accept': friend_request_from_user_accept}

    return render(request, 'users/user_details.html', data)


@login_required
def users_friends_post(request, user_id):
    friend_request_from_user = FriendList.objects.select_related(
        'friend', 'user').filter(friend=request.user, user_id=user_id)

    if not friend_request_from_user.exists():
        user_friend = FriendList.objects.select_related(
            'friend', 'user').filter(user=request.user, friend__id=user_id)

        if user_friend.exists():
            if user_friend.filter(accept=True).exists():
                user_friend = user_friend.first()
                messages.success(request, ('%s %s was deleted from your friend list.') % (user_friend.friend.first_name, user_friend.friend.last_name))
            else:
                user_friend = user_friend.first()
                messages.success(request, ('%s %s friend request was cancelled.') % (user_friend.friend.first_name, user_friend.friend.last_name))         
            
            user_friend.delete()
        else:
            user_friend = FriendList.objects.create(user=request.user, friend_id=user_id)
            messages.success(request, ('A friend request to %s %s was sent successfully.') % (user_friend.friend.first_name, user_friend.friend.last_name))
    else:
        if friend_request_from_user.filter(accept=False).exists():
            decline_or_accept = request.POST.get('accept_decline_friend_request')
            if decline_or_accept == 'accept':
                friend_request_from_user.update(accept=True)
                friend_request_from_user = friend_request_from_user.first()
                messages.success(request, ('The friend request from %s %s was accepted.') % (friend_request_from_user.user.first_name, friend_request_from_user.user.last_name))
            elif decline_or_accept == 'decline':
                friend_request_from_user = friend_request_from_user.first()
                messages.success(request, ('The friend request from %s %s was declined.') % (friend_request_from_user.user.first_name, friend_request_from_user.user.last_name))
                friend_request_from_user.delete()
        else:
            friend_request_from_user = friend_request_from_user.first()
            messages.success(request, ('%s %s was deleted from your friend list.') % (friend_request_from_user.user.first_name, friend_request_from_user.user.last_name))
            friend_request_from_user.delete()

    return redirect('user_details', id=user_id)


class Friends(PaginationMixin, ListView):
    paginate_by = 16
    template_name = 'users/friends.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        accept = self.request.GET.get('accept')

        if accept=='True':
            friends = FriendList.objects.select_related('friend', 'user').filter(
                Q(user=self.request.user) | Q(friend=self.request.user), accept=True)
        elif accept=='False':
            friends = FriendList.objects.select_related('friend', 'user').filter(
                Q(user=self.request.user) | Q(friend=self.request.user), accept=False)
        else:
            friends = FriendList.objects.select_related('friend', 'user').filter(
                Q(user=self.request.user) | Q(friend=self.request.user))

        return friends


class UserSearch(PaginationMixin, ListView):
    paginate_by = 16
    template_name = 'users/user_search.html'
    # filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'first_name', 'last_name', 'email')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        try:
            user_name = self.request.GET.get('user_name')
        except:
            user_name = ''

        if(user_name and user_name != ''):
            friends = User.objects.distinct().exclude(id=self.request.user.id).filter(
                Q(first_name__icontains=user_name) | Q(last_name__icontains=user_name) |
                Q(email__icontains=user_name))
        else:
            friends = User.objects.exclude(id=self.request.user.id)

        return friends