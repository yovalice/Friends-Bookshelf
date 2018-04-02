from django.db import models
from django.contrib.auth.models import AbstractUser

from books.models import Book

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Image(models.Model):
    image = models.ImageField(upload_to='media', blank=True, null=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(100, 100)],
                                     format='JPEG', options={'quality': 60})
    image_small = ImageSpecField(source='image',
                                 processors=[ResizeToFill(160, 160)],
                                 format='JPEG', options={'quality': 60})
    image_medium = ImageSpecField(source='image',
                                  processors=[ResizeToFill(320, 320)],
                                  format='JPEG', options={'quality': 60})
    image_large = ImageSpecField(source='image',
                                 processors=[ResizeToFill(800, 800)],
                                 format='JPEG', options={'quality': 60})

    class Meta:
        abstract = True


class User(AbstractUser, Image):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    bio = models.TextField(max_length=500, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)


class FriendList(models.Model):
    user = models.ForeignKey('users.User', related_name='FriendList_user', on_delete=models.CASCADE)
    friend = models.ForeignKey('users.User', related_name='FriendList_friends', on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)
    decline = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.friend.username


class BookRecommendedByFriend(models.Model):
    friend = models.ForeignKey('users.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.friend.username + ' - ' + self.book
