from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class FriendList(models.Model):
    user = models.ForeignKey(User, related_name='FriendList_user', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='FriendList_friends', on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)
    decline = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.friend.username

class BookRecommendedByFriend(models.Model):
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.friend.username + ' - ' + self.book
