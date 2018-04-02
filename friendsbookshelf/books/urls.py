
from django.urls import path
from .views import books_wishlist, books_liked, books_list, books_detail

urlpatterns = [
    path('wishlist/', books_wishlist, name='books_wishlist'),
    path('liked/', books_liked, name='books_liked'),
    path('', books_list, name='books_list'),
    path('<volume_id>/', books_detail, name='books_detail'),
]
