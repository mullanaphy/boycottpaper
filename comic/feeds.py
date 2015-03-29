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
to john@jo.mu so we can send you a copy immediately.

@copyright Copyright (c) 2014 John Mullanaphy (http://jo.mu/)
@license http://opensource.org/licenses/osl-3.0.php  Open Software License (OSL 3.0)
@author John Mullanaphy <john@jo.mu>
"""

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.conf import settings
from comic.models import Comic


##
# This class is going to give people the latest
#
class ComicFeed(Feed):
    title = "Boycott Paper"
    link = "/"
    description = "Most recent comics."

    def items(self):
        if 'comic_limit' in settings.SITE:
            limit = int(settings.SITE['comic_limit'])
        else:
            limit = 25
        return Comic.objects.order_by('-id')[:limit]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return reverse('comic.views.load_by_slug',
            kwargs={'comic': item.slug, '_format': 'html'})
