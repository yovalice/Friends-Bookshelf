
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import register, forgot, confirm_password

urlpatterns = [
    path('register/', register, name='register'),
    path('forgot/', forgot, name='forgot'),
    path('confirm/', confirm_password, name='confirm_password'),
    path('logout/', auth_views.logout, name='logout'),
]
