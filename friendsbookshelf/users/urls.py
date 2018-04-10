
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import register, login, forgot, confirm_password, EditUserInformation, user_details, Friends

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('forgot/', forgot, name='forgot'),
    path('confirm/', confirm_password, name='confirm_password'),
    path('logout/', auth_views.logout, name='logout'),
    path('user_information/<int:pk>/', EditUserInformation.as_view(), name='user_information'),
    path('user/<int:id>/', user_details, name='user_details'),
    path('user/friends/', Friends.as_view(), name='friends'),
]
