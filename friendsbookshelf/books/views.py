import requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import ListView
from django.utils.decorators import method_decorator

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

from books.models import BooksRead, BookWish


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

    q = request.GET.get('q')
    params = '?maxResults=' + str(max_results) + '&startIndex=' + str(start_index) + '&q=' + q

    books = requests.get(settings.GOOGLE_BOOKS_API + params).json

    return render(request, 'books/list.html',
                  {'books': books,
                   'q': q,
                   'start_index': start_index,
                   'page': page})


@login_required
def books_detail(request, volume_id):
    book = requests.get(settings.GOOGLE_BOOKS_API + volume_id).json

    return render(request, 'books/detail.html',
                  {'book': book})


class BooksWishlist(PaginationMixin, ListView):
    template_name = 'books/wishlist.html'
    paginate_by = 1

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return BookWish.objects.select_related('book').filter(user=self.request.user)


class BooksLiked(PaginationMixin, ListView):
    template_name = 'books/liked.html'
    paginate_by = 1

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return BooksRead.objects.select_related('book').filter(user=self.request.user)