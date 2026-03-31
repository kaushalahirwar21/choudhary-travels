from django.contrib import admin
from django.urls import path
from booking import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('book/', views.book),
    path('about/', views.about),
    path('secure-login/', admin.site.urls),
]    


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


