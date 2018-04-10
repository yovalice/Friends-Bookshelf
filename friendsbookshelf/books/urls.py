
from django.urls import path, re_path
from .views import BooksWishlist, BooksLiked, books_list, books_detail, books_like_dislike_post, books_wishlist_post

urlpatterns = [
    path('wishlist/', BooksWishlist.as_view(), name='books_wishlist'),
    path('liked/', BooksLiked.as_view(), name='books_liked'),
    path('', books_list, name='books_list'),
    path('<volume_id>/', books_detail, name='books_detail'),
    re_path('books_like_dislike_post/(?P<volume_id>\w+)/(?P<book_name>\w+)/', books_like_dislike_post, name='books_like_dislike_post'),
    re_path('books_wishlist_post/(?P<volume_id>\w+)/(?P<book_name>\w+)/', books_wishlist_post, name='books_wishlist_post'),
]

