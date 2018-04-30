
from django.urls import path
from .views import post_comment, home_page, delete_post, load_more_posts

urlpatterns = [
    path('', home_page, name='home'),
    path('ajax/comment/', post_comment, name='ajax_post_comments'),
    path('delete/post/<int:post_id>', delete_post, name='delete_post'),
    path('ajax/comment/<int:page>', load_more_posts, name='load_more_posts'),
]


