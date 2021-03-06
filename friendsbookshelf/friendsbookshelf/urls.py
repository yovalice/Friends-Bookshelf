from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from main_app.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('books/', include('books.urls')),
    path('', include('main_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
