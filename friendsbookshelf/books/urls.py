
from django.urls import path
from .views import BooksWishlist, BooksLiked, books_list, books_detail, books_like_dislike_post, books_wishlist_post

urlpatterns = [
    path('wishlist/', BooksWishlist.as_view(), name='books_wishlist'),
    path('liked/', BooksLiked.as_view(), name='books_liked'),
    path('', books_list, name='books_list'),
    path('<volume_id>/', books_detail, name='books_detail'),
    path('books_like_dislike_post/<volume_id>/<book_name>', books_like_dislike_post, name='books_like_dislike_post'),
    path('books_wishlist_post/<volume_id>/', books_wishlist_post, name='books_wishlist_post'),
]

