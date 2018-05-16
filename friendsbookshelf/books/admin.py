from django.contrib import admin
from .models import Book
from .models import BooksRead 
from .models import BookWish
from main_app.actions import export_as_csv_action


class BookAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'google_id']
    list_display = ('id', 'name', 'google_id')
    list_display_links = ('id', 'name', 'google_id')
    actions = [export_as_csv_action("CSV Export", fields=['id', 'name'])]


class BooksReadsAdmin(admin.ModelAdmin):
    search_fields = ['id', 'book__name', 'book__google_id', 'user__username']
    list_display = ('id', 'book', 'user', 'liked')
    list_display_links = ('id', 'book')
    list_filter = ('liked',)
    list_select_related = ('book', 'user')
    raw_id_fields = ('user', 'book')
    actions = [export_as_csv_action("CSV Export", fields=['id', 'book', 'user', 'liked'])]


class BookWishAdmin(admin.ModelAdmin):
    search_fields = ['id', 'book__name', 'book__google_id', 'user__username']
    list_display = ('id', 'book', 'user')
    list_display_links = ('id', 'book')
    list_select_related = ('book', 'user')
    raw_id_fields = ('user', 'book')
    actions = [export_as_csv_action("CSV Export", fields=['id', 'book', 'user'])]


admin.site.register(Book, BookAdmin)
admin.site.register(BooksRead, BooksReadsAdmin)
admin.site.register(BookWish, BookWishAdmin)
