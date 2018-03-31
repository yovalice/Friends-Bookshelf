from django.contrib.auth.models import User
from django.db import models
from books.models import Book

class Post(models.Model):
    description = models.TextField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comments = models.ManyToManyField('main_app.Comment', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + self.description

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + self.text
