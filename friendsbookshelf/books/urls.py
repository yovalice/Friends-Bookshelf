
from django.urls import path
from .views import books_wishlist, books_liked

urlpatterns = [
    path('books_wishlist/', books_wishlist, name='books_wishlist'),
    path('books_liked/', books_liked, name='books_liked'),
]
