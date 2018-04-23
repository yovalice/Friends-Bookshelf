
from django.urls import path, re_path
from .views import (BooksWishlist, BooksLiked, books_list, books_detail,
                    books_like_dislike_post, books_wishlist_post, books_recommend_post,
                    RecommendedBooks)

urlpatterns = [
    path('wishlist/', BooksWishlist.as_view(), name='books_wishlist'),
    path('liked/', BooksLiked.as_view(), name='books_liked'),
    path('recommended_books/', RecommendedBooks.as_view(), name='recommended_books'),
    path('', books_list, name='books_list'),
    path('<volume_id>/', books_detail, name='books_detail'),
    path('books_like_dislike_post/<volume_id>/<book_name>/', books_like_dislike_post, name='books_like_dislike_post'),
    path('books_wishlist_post/<volume_id>/<book_name>/', books_wishlist_post, name='books_wishlist_post'),
    path('books_recommend_post/<volume_id>/<book_name>/<int:user_id>', books_recommend_post, name='books_recommend_post'),
]

