from django.conf.urls import patterns, url

urlpatterns = patterns('user.views',
    (r'^$', 'index'),
    (r'^(?P<user>\d+)/$', 'load_by_pk', {'_format': 'html'}),
    (r'^(?P<user>[a-zA-Z0-9_-]+)/$', 'load_by_slug', {'_format': 'html'}),
    (r'^(?P<user>\d+).json$', 'load_by_pk', {'_format': 'json'}),
    (r'^(?P<user>[a-zA-Z0-9_-]+).json$', 'load_by_slug', {'_format': 'json'}),
)
