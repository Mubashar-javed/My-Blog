
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from blog.sitemaps import PostSiteMap
from blog.views import post_list

sitemaps = {
    'posts': PostSiteMap,
}

urlpatterns = [
    path('realadmin/docs/', include('django.contrib.admindocs.urls')),
    path('realadmin/', admin.site.urls),

    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('sitemap.xml', sitemap, {
         'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', post_list, name='index')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
