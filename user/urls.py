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


# We have three endpoints, for to view all users with pagination, second to
# load a user by their id and latestly to load them by their username.
urlpatterns = patterns('user.views',
    (r'^$', 'index'),
    (r'^(?P<user>\d+).(?P<_format>[a-zA-Z0-9_-]+)$', 'load_by_pk'),
    (r'^(?P<user>[a-zA-Z0-9_-]+).(?P<_format>[a-zA-Z0-9_-]+)$', 'load_by_slug'),
)
