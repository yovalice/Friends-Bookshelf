
from django.urls import path
from .views import post_comment, home_page

urlpatterns = [
    path('', home_page, name='home'),
    path('ajax/comment/', post_comment, name='ajax_post_comments'),
    # path('ajax/comment/', views.load_more_posts, name='ajax_load_more_posts'),
]


