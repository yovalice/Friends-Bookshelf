
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (register, login, forgot, user_reset_password,
                    EditUserInformation, user_details, Friends,
                    users_friends_post, UserSearch)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('forgot/', forgot, name='forgot'),
    path('user_reset_password/<uid>/<token>/', user_reset_password, name='user_reset_password'),
    path('logout/', auth_views.logout, name='logout'),
    path('user_information/<int:pk>/', EditUserInformation.as_view(), name='user_information'),
    path('user/<int:id>/', user_details, name='user_details'),
    path('user/add_remove/<int:user_id>/', users_friends_post, name='users_friends_post'),
    path('user/friends/', Friends.as_view(), name='friends'),
    path('user/user_search/', UserSearch.as_view(), name='user_search'),
]
