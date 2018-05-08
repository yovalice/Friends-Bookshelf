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
    '''
        This is the Home page and newsfeed (if the user is logged in) page logic.
    '''
    # Books suggestion array
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
        'Math',
        'paulo coelho',
        'hunger games',
        '100 años de soledad',
        'Gabriel García Márquez'
    ]

    # Get one random value from the books suggestions array
    q = random.choice(books_array)

    # Setup parameters for the google api call
    params = '?maxResults=6&q=' + q + '&fields=items/volumeInfo/title,items/volumeInfo/imageLinks,items/id'

    # Get books from google api call
    books = requests.get(settings.GOOGLE_BOOKS_API + params).json

    # If the user is logged in send the user to the newsfeed
    if request.user.is_authenticated:
        # If the user in the newsfeed inserted a new post.
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
            # Load the post Form
            form = UserPostForm(request.user)

        # Get user friend list to check
        friend_list = FriendList.objects.select_related(
            'friend', 'user').filter(Q(user=request.user) | Q(friend=request.user))

        # Get all the friends and user posts inserted ordered by the most recent one
        posts = Post.objects.distinct().select_related('book', 'book__book', 'user').prefetch_related(
            'comments', 'comments__user').filter(Q(user=request.user) |
                    Q(user__in=friend_list.filter(accept=True).values_list('friend__pk', flat=True)) |
                    Q(user__in=friend_list.filter(accept=True).values_list('user__pk', flat=True))
                    ).order_by('-created_date')[:8]

        # Start friend suggest logic (based on books both likes)
        users_from_friend_list = User.objects.filter(
            Q(pk__in=friend_list.values_list('friend__pk', flat=True)) | Q(pk__in=friend_list.values_list('user__pk', flat=True)))

        my_books_read = BooksRead.objects.filter(user=request.user, liked=True)

        friends_with_books_read = BooksRead.objects.distinct().filter(
            book__in=my_books_read.values_list('book__pk', flat=True)).values_list('user__pk', flat=True)

        friends_suggest = User.objects.filter(pk__in=friends_with_books_read).exclude(
            Q(pk=request.user.pk) |
            Q(pk__in=users_from_friend_list.values_list('pk', flat=True)))[:6]
        # End friend Suggest list

        return render(request, 'newsfeed.html', {'posts': posts, 'friends_suggest': friends_suggest, 'form': form, 'books': books})
    else:
        return render(request, 'home.html',
                    {'books': books})


@csrf_exempt
def post_comment(request):
    '''
        This is the insert comment into a post logic from the newsfeed.
    '''
    if request.is_ajax():
        # Get text value from the input
        text = request.POST.get('text')

        # Create new comment
        comment = Comment.objects.create(text=text, user=request.user)

        # Get post and add the comment to the post
        post = Post.objects.get(id=request.POST.get('post_id'))
        post.comments.add(comment)

        return JsonResponse({'text': text, 'user_id': request.user.id, 'full_name': request.user.first_name + ' ' + request.user.last_name})


@csrf_exempt
def delete_post(request, post_id):
    '''
        This is the Delete Post logic from the newsfeed.
    '''
    # Delete post call
    Post.objects.get(id=post_id, user=request.user).delete()
    messages.success(request, 'Your post was deleted successfully.')
    return redirect('home') 


def load_more_posts(request, page):
    '''
        Load more posts ajax call.
    '''
    if request.is_ajax():
        friend_list = FriendList.objects.select_related(
            'friend').filter(user=request.user, accept=True).values_list('friend', flat=True)

        objects = Post.objects.select_related('book', 'book__book', 'user').prefetch_related(
            'comments', 'comments__user').filter(Q(user=request.user) | Q(user__in=friend_list)).order_by('-created_date')

        paginator = Paginator(objects, 8)

        posts = paginator.page(int(page))

        return JsonResponse({'posts': serializers.serialize("json", posts.object_list), 'has_next': posts.has_next()})