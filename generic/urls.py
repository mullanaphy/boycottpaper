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


# Paths to /, /about, and /search?q=. They're all pretty standard "generic"
# paths so no need to muck up the code base elsewhere.
urlpatterns = patterns('generic.views',
    (r'^$', 'index'),
    (r'^search$', 'search'),
    (r'^about$', 'about'),
)
