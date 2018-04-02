
from django.urls import path

from .views import books_list, books_detail

urlpatterns = [
    path('', books_list, name='books_list'),
    path('<volume_id>/', books_detail, name='books_detail'),
]
