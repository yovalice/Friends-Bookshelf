from django.contrib import admin
from .models import Book
from .models import BooksRead 
from .models import BookWish


class BookAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'google_id']
    list_display = ('id', 'name', 'google_id')
    list_display_links = ('id', 'name', 'google_id')


class BooksReadsAdmin(admin.ModelAdmin):
    search_fields = ['id', 'book__name', 'book__google_id', 'user__username']
    list_display = ('id', 'book', 'user', 'liked')
    list_display_links = ('id', 'book')
    list_filter = ('liked',)


class BookWishAdmin(admin.ModelAdmin):
    search_fields = ['id', 'book__name', 'book__google_id', 'user__username']
    list_display = ('id', 'book', 'user')
    list_display_links = ('id', 'book')


admin.site.register(Book, BookAdmin)
admin.site.register(BooksRead, BooksReadsAdmin)
admin.site.register(BookWish, BookWishAdmin)
