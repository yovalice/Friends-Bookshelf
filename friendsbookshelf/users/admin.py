from django.contrib import admin
from .models import FriendList
from .models import BookRecommendedByFriend
from .models import User


class FriendListAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user', 'friend', 'created_date']
    list_display = ('id', 'user', 'friend', 'accept', 'created_date')
    list_display_links = ('id', 'user', 'friend')
    list_filter = ('accept',)
    raw_id_fields = ('user', 'friend')


class BookRecommendedByFriendAdmin(admin.ModelAdmin):
    search_fields = ['id', 'friend']
    list_display = ('id', 'friend', 'book')
    list_display_links = ('id', 'friend', 'book')


class UserAdmin(admin.ModelAdmin):
    search_fields = ['id', 'username', 'first_name', 'last_name', 'email']
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    list_display_links = ('id', 'username')
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(FriendList, FriendListAdmin)
admin.site.register(BookRecommendedByFriend, BookRecommendedByFriendAdmin)
admin.site.register(User, UserAdmin)
