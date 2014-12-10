"""
Boycott Paper

LICENSE

This source file is subject to the Open Software License (OSL 3.0)
that is bundled with this package in the file LICENSE.txt.
It is also available through the world-wide-web at this URL:
http://opensource.org/licenses/osl-3.0.php
If you did not receive a copy of the license and are unable to
obtain it through the world-wide-web, please send an email
to john@jo.mu so we can send you a copy immediately.

@copyright Copyright (c) 2014 John Mullanaphy (http://jo.mu/)
@license http://opensource.org/licenses/osl-3.0.php  Open Software License (OSL 3.0)
@author John Mullanaphy <john@jo.mu>
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()

# We need to load generic which handles our index, search, and about page. Then
# comic, and user which both handle their own models. Besides that just the
# usual stuff, media, resources, admin panel, and favicon.
urlpatterns = patterns('',
    (r'^', include('generic.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_URL}),
    (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
    (r'^comic/', include('comic.urls')),
    (r'^user/', include('user.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^favicon\.ico$', RedirectView.as_view(url=settings.MEDIA_URL + 'favicon.png')),
)
