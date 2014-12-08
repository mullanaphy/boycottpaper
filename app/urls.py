from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('generic.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_URL}),
    (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
    (r'^comic/', include('comic.urls')),
    (r'^user/', include('user.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^favicon\.ico$', RedirectView.as_view(url=settings.MEDIA_URL + 'favicon.ico')),
)