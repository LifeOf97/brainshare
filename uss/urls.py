from django.contrib.sitemaps.views import sitemap
from django.conf.urls.static import static
from django.urls import path, include
from .sitemaps import PostSitemap
from django.contrib import admin
from django.conf import settings

sitemaps = {
    'post': PostSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userapp.urls')),
    path('', include('blogapp.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
