from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from booking import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('book/', views.book),
    path('about/', views.about),
    path('admin/', admin.site.urls),
    path('secure-login/', RedirectView.as_view(url='/admin/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
