from django.contrib import admin
from .models import FriendList
from .models import BookRecommendedByFriend

class FriendListAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user', 'friend', 'created_date']
    list_display = ('id', 'user', 'friend', 'accept', 'decline', 'created_date')
    list_display_links = ('id', 'user', 'friend')
    list_filter = ('accept', 'decline')

class BookRecommendedByFriendAdmin(admin.ModelAdmin):
    search_fields = ['id', 'friend']
    list_display = ('id', 'friend', 'book')
    list_display_links = ('id', 'friend', 'book')

admin.site.register(FriendList, FriendListAdmin)
admin.site.register(BookRecommendedByFriend, BookRecommendedByFriendAdmin)