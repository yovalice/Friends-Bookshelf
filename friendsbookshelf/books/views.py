import requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

from pure_pagination.mixins import PaginationMixin

from books.models import Book, BooksRead, BookWish


def books_list(request):
    max_results = 40

    try:
        page = int(request.GET.get('page', 1))

        if int(page >= 2):
            start_index = int(max_results) * (page-1)
        else:
            start_index = '0'

    except PageNotAnInteger:
        start_index = '0'

    q = request.POST.get('q')
    params = '?maxResults=' + str(max_results) + '&startIndex=' + str(start_index) + '&q=' + q

    books = requests.get(settings.GOOGLE_BOOKS_API + params).json

    return render(request, 'books/list.html',
                  {'books': books,
                   'q': q,
                   'start_index': start_index,
                   'page': page})


@login_required
def books_detail(request, volume_id):
    book = requests.get(settings.GOOGLE_BOOKS_API + volume_id).json()

    read = BooksRead.objects.filter(book__google_id=book['id'])
    wishlist = BookWish.objects.filter(book__google_id=book['id']).exists()

    return render(request, 'books/detail.html',
                  {'book': book,
                   'read': read,
                   'wishlist': wishlist})


@login_required
def books_like_dislike_post(request, volume_id, book_name):
    liked_var = request.POST.get('liked')
    
    book_liked = BooksRead.objects.filter(user=request.user, book__google_id=volume_id).exists()

    if liked_var == 'True':
        liked = True
    else:
        liked = False

    if book_liked:
        book_liked.update(liked=liked)
    else:
        book = Book.objects.filter(google_id=volume_id)

        if book.exists():
            BooksRead.objects.create(user=request.user, book=book.first(), liked=liked)
        else:
            book_created = Book.objects.create(name=book_name, google_id=volume_id)
            BooksRead.objects.create(user=request.user, book=book_created, liked=liked)

    return redirect('books_detail', volume_id=volume_id)


@login_required
def books_wishlist_post(request, volume_id, book_name):    
    book_liked = BookWish.objects.filter(user=request.user, book__google_id=volume_id).exists()
    book = Book.objects.filter(google_id=volume_id)

    if book_liked:
        if book.exists():
            BookWish.objects.create(user=request.user, book=book.first())
        else:
            book_created = Book.objects.create(name=book_name, google_id=volume_id)
            BookWish.objects.create(user=request.user, book=book_created)
    else:
        book_liked.delete()

    return redirect('books_detail', volume_id=volume_id)


class BooksWishlist(PaginationMixin, ListView):
    template_name = 'books/wishlist.html'
    paginate_by = 9

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return BookWish.objects.select_related('book').filter(user=self.request.user)


class BooksLiked(PaginationMixin, ListView):
    template_name = 'books/liked.html'
    paginate_by = 9

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return BooksRead.objects.select_related('book').filter(user=self.request.user)