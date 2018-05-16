from django.contrib import admin
from .models import FriendList
from .models import BookRecommendedByFriend
from .models import User
from main_app.actions import export_as_csv_action


class FriendListAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user', 'friend', 'created_date']
    list_display = ('id', 'user', 'friend', 'accept', 'created_date')
    list_display_links = ('id', 'user', 'friend')
    list_filter = ('accept',)
    raw_id_fields = ('user', 'friend')
    list_select_related = ('user', 'friend')
    actions = [export_as_csv_action("CSV Export", fields=['id', 'user', 'friend', 'accept', 'created_date'])]


class BookRecommendedByFriendAdmin(admin.ModelAdmin):
    search_fields = ['id', 'friend', 'user']
    list_display = ('id', 'friend', 'user', 'book')
    list_display_links = ('id', 'friend', 'user', 'book')
    list_select_related = ('book', 'friend', 'user')
    raw_id_fields = ('book', 'friend', 'user')
    actions = [export_as_csv_action("CSV Export", fields=['id', 'friend', 'user', 'book'])]


class UserAdmin(admin.ModelAdmin):
    search_fields = ['id', 'username', 'first_name', 'last_name', 'email']
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    list_display_links = ('id', 'username')
    filter_horizontal = ('groups', 'user_permissions')
    actions = [export_as_csv_action("CSV Export", fields=['id', 'username', 'first_name', 'last_name', 'email'])]


admin.site.register(FriendList, FriendListAdmin)
admin.site.register(BookRecommendedByFriend, BookRecommendedByFriendAdmin)
admin.site.register(User, UserAdmin)
