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

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def site(name):
    if name in settings.SITE:
        return settings.SITE[name]
    else:
        return ""


@register.simple_tag
def google_analytics():
    if 'google_analytics' in settings.SITE:
        code = """<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', '""" + settings.SITE['google_analytics'] + """', 'auto');
  ga('send', 'pageview');

</script>"""
        return code
    else:
        return ""


@register.simple_tag
def facebook_api():
    if 'facebook_api' in settings.SITE:
        code = """<div id="fb-root"></div>
  <script>(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&appId=""" + str(settings.SITE['facebook_api']) + """&version=v2.0";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));</script>"""
        return code
    else:
        return ""


@register.simple_tag
def addthis_init():
    if 'addthis' in settings.SITE:
        return '<script type="text/javascript" src="//s7.addthis.com/js/300/addthis_widget.js#pubid=' + settings.SITE[
            'addthis'] + '" async="async"></script>'
    else:
        return ""


@register.simple_tag
def addthis_toolbox():
    if 'addthis' in settings.SITE:
        return '<div class="addthis_sharing_toolbox"></div>'
    else:
        return ''


@register.simple_tag
def social_media():
    if 'social' in settings.SITE:
        code = '<div class="pull-right"><ul class="list-inline">'
        for social in settings.SITE['social']:
            code += '<li><a href="' + social[2] + '"><span class="fa fa-' + social[0]
            code += '"></span><span class="hidden-xs"> ' + social[1] + '</span></a></li>'
        code += '</ul></div>'
        return code
    else:
        return ''


@register.filter
def number_range(number, limit):
    if limit:
        return range(number - limit, number + limit)
    else:
        return range(1, number)
