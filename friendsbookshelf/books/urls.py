
from django.urls import path
from .views import BooksWishlist, BooksLiked, books_list, books_detail

urlpatterns = [
    path('wishlist/', BooksWishlist.as_view(), name='books_wishlist'),
    path('liked/', BooksLiked.as_view(), name='books_liked'),
    path('', books_list, name='books_list'),
    path('<volume_id>/', books_detail, name='books_detail'),
]
