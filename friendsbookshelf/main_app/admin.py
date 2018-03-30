from django.contrib import admin
from .models import Post
from .models import Comment

class PostAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user', 'created_date']
    list_display = ('id', 'user', 'description', 'created_date')
    list_display_links = ('id', 'user')
    filter_horizontal = ('comments',)

class CommentAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user', 'created_date']
    list_display = ('id', 'user', 'text', 'created_date')
    list_display_links = ('id', 'user')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
