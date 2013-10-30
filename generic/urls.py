from django.conf.urls import patterns, url

urlpatterns = patterns('generic.views',
    (r'^$', 'index'),
    (r'^search$', 'search'),
    (r'^about$', 'about'),
)
