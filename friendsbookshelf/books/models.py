from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    name = models.TextField()
    isbn = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.isbn)


class BookWish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.book.isbn)


class BooksRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    liked = models.BooleanField()

    def __str__(self):
        return str(self.book.isbn)
