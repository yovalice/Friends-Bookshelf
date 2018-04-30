import requests
import random

from django.conf import settings
from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.core import serializers

from django.core.paginator import Paginator

from main_app.models import Post, Comment
from books.models import BooksRead
from users.models import FriendList, User
from users.forms import UserLoginForm, UserRegisterForm
from main_app.forms import UserPostForm


def home_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserPostForm(user=request.user, data=request.POST)

            if form.is_valid():
                post = form.cleaned_data['post']
                book = form.cleaned_data['book_choice']

                if not book:
                    book = None
                    
                Post.objects.create(description=post, user=request.user, book=book)
                
                messages.success(request, 'Your post was submitted successfully.')

                return HttpResponseRedirect('/')
        else:
            form = UserPostForm(request.user)

        friend_list = FriendList.objects.select_related(
            'friend').filter(Q(user=request.user) | Q(friend=request.user), accept=True).values_list('friend', flat=True)

        posts = Post.objects.select_related('book', 'book__book', 'user').prefetch_related(
            'comments', 'comments__user').filter(Q(user=request.user) | Q(user__in=friend_list)).order_by('-created_date')[:8]

        my_books_read = BooksRead.objects.filter(user=request.user).values_list('book__pk', flat=True)

        print(my_books_read)

        friends_with_books_read = BooksRead.objects.exclude(
            user__in=friend_list, book__in=my_books_read).exclude(
                user=request.user).values_list('user__pk', flat=True)

        print(friends_with_books_read)

        friends_suggest = User.objects.filter(pk__in=friends_with_books_read)

        print(friends_suggest)

        return render(request, 'newsfeed.html', {'posts': posts, 'friends_suggest': friends_suggest, 'form': form})
    else:
        books_array = [
            'Harry Potter',
            'Lord of the rings',
            'Game of Thrones',
            'A walk to Remember',
            'Emily Griffin',
            'Pride and Prejudice',
            'Comic books',
            'Manga',
            'Les Miserables',
            'Graphic Novels',
            'Romantic Comedy',
            'Romantic',
            'Horror',
            'Comedy',
            'Video Games',
            'University Book',
            'Biology',
            'Math'
        ]

        q = random.choice(books_array)

        params = '?maxResults=6&q=' + q + '&fields=items/volumeInfo/title,items/volumeInfo/imageLinks,items/id'

        books = requests.get(settings.GOOGLE_BOOKS_API + params).json

        return render(request, 'home.html',
                    {'books': books})


def load_more_posts(request, page):
    if request.is_ajax():
        friend_list = FriendList.objects.select_related(
            'friend').filter(user=request.user, accept=True).values_list('friend', flat=True)

        objects = Post.objects.select_related('book', 'book__book', 'user').prefetch_related(
            'comments', 'comments__user').filter(Q(user=request.user) | Q(user__in=friend_list)).order_by('-created_date')

        paginator = Paginator(objects, 8)

        posts = paginator.page(int(page))

        print(posts.has_next())
        print(posts)

        return JsonResponse({'posts': serializers.serialize("json", posts.object_list), 'has_next': posts.has_next()})


@csrf_exempt
def post_comment(request):
    if request.is_ajax():
        text = request.POST.get('text')
        comment = Comment.objects.create(text=text, user=request.user)
        post = Post.objects.get(id=request.POST.get('post_id'))
        post.comments.add(comment)
        return JsonResponse({'text': text, 'user_id': request.user.id, 'full_name': request.user.first_name + ' ' + request.user.last_name})


@csrf_exempt
def delete_post(request, post_id):
    Post.objects.get(id=post_id, user=request.user).delete()
    messages.success(request, 'Your post was deleted successfully.')
    return redirect('home') 