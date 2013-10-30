from django.conf.urls import patterns, url

urlpatterns = patterns('comic.views',
    (r'^$', 'index'),
    (r'^first$', 'first'),
    (r'^latest$', 'latest'),
    (r'^popular$', 'popular'),
    (r'^random$', 'random'),
    (r'^(?P<comic>\d+).(?P<_format>[a-zA-Z0-9_-]+)$', 'load_by_pk'),
    (r'^(?P<comic>[a-zA-Z0-9_-]+).(?P<_format>[a-zA-Z0-9_-]+)$', 'load_by_slug'),
)
