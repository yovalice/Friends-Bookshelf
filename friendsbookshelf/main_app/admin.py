from django.contrib import admin
from .models import Post
from .models import Comment

class PostAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user', 'created_date']
    list_display = ('id', 'user', 'description', 'created_date')
    list_display_links = ('id', 'user')
    filter_horizontal = ('comments',)
    list_select_related = ('user', 'book')
    raw_id_fields = ('user', 'book', 'comments')


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user', 'created_date']
    list_display = ('id', 'user', 'text', 'created_date')
    list_display_links = ('id', 'user')
    list_select_related = ('user',)
    raw_id_fields = ('user',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
