import requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q

from pure_pagination.mixins import PaginationMixin

from users.models import User
from .models import Book, BooksRead, BookWish
from users.models import BookRecommendedByFriend, FriendList


def books_list(request):
    '''
        Search books page page.
    '''
    # Get Search Value
    q = request.GET.get('q')

    # Set parameters for api call
    params = '?maxResults=39&q=' + q + '&fields=items/volumeInfo/title,items/volumeInfo/imageLinks,items/id'

    # Get books from api call in json format
    books = requests.get(settings.GOOGLE_BOOKS_API + params).json

    return render(request, 'books/list.html',
                  {'books': books,
                   'q': q})


def books_detail(request, volume_id):
    '''
        Book detail page page.
    '''
    # Google api call to get the book information
    book = requests.get(settings.GOOGLE_BOOKS_API + volume_id).json()

    # If the user is logged in check if he liked/disliked, added to wishlist the book
    if request.user.is_authenticated:
        read = BooksRead.objects.filter(user=request.user, book__google_id=volume_id).first()
        wishlist = BookWish.objects.filter(user=request.user, book__google_id=volume_id).exists()
        friends = FriendList.objects.select_related('friend', 'user').filter(
            Q(user=request.user) | Q(friend=request.user), accept=True)
    else:
        read = None
        wishlist = None
        friends = None

    return render(request, 'books/detail.html',
                  {'book': book,
                   'read': read,
                   'wishlist': wishlist,
                   'friends': friends})


class BooksWishlist(PaginationMixin, ListView):
    '''
        Book user added to Wishlist list page.
    '''
    template_name = 'books/wishlist.html'
    paginate_by = 6

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        # Get all the Bookwish from the logged in user
        return BookWish.objects.select_related('book').filter(user=self.request.user)


class BooksLiked(PaginationMixin, ListView):
    '''
        Book users Liked list page.
    '''
    template_name = 'books/liked.html'
    paginate_by = 6

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        # Get liked filter
        liked = self.request.GET.get('liked')

        # If there is no filter, get all the Books Liked from the logged in user,
        # if the liked filter is True get only the book the user liked
        # if the liked filter is False get only the book the user dosen't liked
        if liked=='True':
            books_read = BooksRead.objects.select_related('book').filter(user=self.request.user, liked=True)
        elif liked=='False':
            books_read = BooksRead.objects.select_related('book').filter(user=self.request.user, liked=False)
        else:
            books_read = BooksRead.objects.select_related('book').filter(user=self.request.user)

        return books_read


class RecommendedBooks(PaginationMixin, ListView):
    '''
        Book Recommended by other users page.
    '''
    template_name = 'books/recommended_books.html'
    paginate_by = 6

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        # Get all the recommended Books from the logged in user
        recommended_books = BookRecommendedByFriend.objects.select_related(
            'book', 'friend', 'user').filter(user=self.request.user)

        return recommended_books


@login_required
def books_like_dislike_post(request, volume_id, book_name):
    '''
        Book Like/Dislike button logic.
    '''
    liked_var = request.POST.get('liked')

    book_liked = BooksRead.objects.filter(user=request.user, book__google_id=volume_id)

    if liked_var == 'True':
        liked = True
    else:
        liked = False

    if book_liked.exists():
        book_liked.update(liked=liked)
        messages.success(request, 'The book with the title ' + book_name + ' was updated.')
    else:
        book = Book.objects.filter(google_id=volume_id)

        if book.exists():
            BooksRead.objects.create(user=request.user, book=book.first(), liked=liked)
        else:
            book_created = Book.objects.create(name=book_name, google_id=volume_id)
            BooksRead.objects.create(user=request.user, book=book_created, liked=liked)

        messages.success(request, 'The book with the title ' + book_name + ' was added to book reads list.')

    return redirect('books_detail', volume_id=volume_id)


@login_required
def books_wishlist_post(request, volume_id, book_name):
    '''
        Book Wishlist button logic.
    '''
    book_liked = BookWish.objects.filter(user=request.user, book__google_id=volume_id)

    if book_liked.exists():
        book_liked.delete()
        messages.success(request, 'The book with the title ' + book_name + ' was removed from the books wishlist.')
    else:
        book = Book.objects.filter(google_id=volume_id)
        if book.exists():
            BookWish.objects.create(user=request.user, book=book.first())
        else:
            book_created = Book.objects.create(name=book_name, google_id=volume_id)
            BookWish.objects.create(user=request.user, book=book_created)

        messages.success(request, 'The book with the title ' + book_name + ' was added to the books wishlist.')
    return redirect('books_detail', volume_id=volume_id)


@login_required
def books_recommend_post(request, volume_id, book_name, user_id):
    '''
        Recommended books post logic
    '''
    recommended_book = BookRecommendedByFriend.objects.select_related(
        'book', 'friend', 'user').filter(user=user_id, friend=request.user, book__google_id=volume_id)
    user = User.objects.get(id=user_id)

    if recommended_book.exists():
        messages.error(request, 'The book with the title ' + book_name + ' was already recommended to the user ' + user.first_name + ' ' + user.last_name + '.')
    else:
        book = Book.objects.filter(google_id=volume_id)

        if book.exists():
            BookRecommendedByFriend.objects.create(user=user, friend=request.user, book=book.first())
        else:
            book_created = Book.objects.create(name=book_name, google_id=volume_id)
            BookRecommendedByFriend.objects.create(user=user, friend=request.user, book=book_created)

        messages.success(request, 'The book with the title ' + book_name + ' was recommended to the user ' + user.first_name + ' ' + user.last_name + '.')
    return redirect('books_detail', volume_id=volume_id)