# -*- coding: utf-8 -*-
"""
Boycott Paper

LICENSE

This source file is subject to the Open Software License (OSL 3.0)
that is bundled with this package in the file LICENSE.txt.
It is also available through the world-wide-web at this URL:
http://opensource.org/licenses/osl-3.0.php
If you did not receive a copy of the license and are unable to
obtain it through the world-wide-web, please send an email
to hi@john.mu so we can send you a copy immediately.

@copyright Copyright (c) 2014 John Mullanaphy (https://john.mu/)
@license http://opensource.org/licenses/osl-3.0.php  Open Software License (OSL 3.0)
@author John Mullanaphy <hi@john.mu>
"""

from django.conf.urls import patterns, url


# The main routes here are the index which counts as our archives and our two
# load_by routes which load actual comics. All the other routes will do a tiny
# bit of code to and redirect to load_by_slug when it finds the appropriate
# Comic model to use.
urlpatterns = patterns('comic.views',
    (r'^$', 'index'),
    (r'^first$', 'first'),
    (r'^latest$', 'latest'),
    (r'^popular$', 'popular'),
    (r'^random$', 'random'),
    (r'^(?P<comic>\d+).(?P<_format>[a-zA-Z0-9_-]+)$', 'load_by_pk'),
    (r'^(?P<comic>[a-zA-Z0-9_-]+).(?P<_format>[a-zA-Z0-9_-]+)$', 'load_by_slug'),
)
