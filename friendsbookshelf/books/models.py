from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    name = models.TextField()
    google_id = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' - ' + self.google_id


class BookWish(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book.name


class BooksRead(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    liked = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book.name
