import requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from books.models import BooksRead, BookWish

api_url = 'https://www.googleapis.com/books/v1/volumes/'


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

    books = requests.get(api_url + params)

    return render(request, 'books/list.html',
                  {'books': books.json,
                   'q': q,
                   'start_index': start_index,
                   'page': page})


@login_required
def books_detail(request, volume_id):
    book = requests.get(api_url + volume_id).json

    return render(request, 'books/detail.html',
                  {'book': book})


@login_required
def books_wishlist(request):
    BookWish.objects.select_related(
        'user', 'book').filter(user=request.user)
    return render(request, 'books/books_wishlist.html')


@login_required
def books_liked(request):
    BooksRead.objects.select_related(
        'user', 'book').filter(user=request.user)
    return render(request, 'books/books_liked.html')
