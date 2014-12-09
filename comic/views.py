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

from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import json as simplejson
import random as randomint
from comic.models import Comic


##
# Load an index page listing all of our comics.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def index(request):
    collection = Comic.objects.all().order_by('-created')[:3]
    t = loader.get_template('comic/collection.html')
    c = Context({'collection': collection, })
    return HttpResponse(t.render(c))


##
# Return my first comic ever.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def first(request):
    comic = Comic.objects.all().order_by('created')[0]
    return redirect('comic.views.load_by_slug', comic=comic.slug, _format='html')


##
# Return the latest comic.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def latest(request):
    comic = Comic.objects.all().order_by('-created')[0]
    return redirect('comic.views.load_by_slug', comic=comic.slug, _format='html')


##
# Return all popular comics.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def popular(popular):
    comic_list = Comic.objects.all().order_by('-karma')[:5]
    t = loader.get_template('comic/collection.html')
    c = Context({'comic_list': comic_list, })
    return HttpResponse(t.render(c))


##
# Randomly select a comic and then redirect to its canonical url.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def random(request):
    count = Comic.objects.all().count()
    i = randomint.random() * count + 1
    comic = Comic.objects.get(pk=i)
    return redirect('comic.views.load_by_slug', comic=comic.slug, _format='html')


##
# Load a Comic by its comic_id.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def load_by_pk(request, comic, _format='html'):
    if _format == 'json':
        try:
            comic = Comic.objects.get(pk=comic)
            return json_response(comic)
        except Comic.DoesNotExist as e:
            return HttpResponse(simplejson.dumps({"error": str(e), }), mimetype="application/json", status=404)
            pass
    else:
        comic = get_object_or_404(Comic, pk=comic)
        return html_response(comic)


##
# Load a Comic by its slug.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def load_by_slug(request, comic, _format='html'):
    if _format == 'json':
        try:
            comic = Comic.objects.get(slug=comic)
            return json_response(comic)
        except Comic.DoesNotExist as e:
            return HttpResponse(simplejson.dumps({"error": str(e), }), mimetype="application/json", status=404)
            pass
    else:
        comic = get_object_or_404(Comic, slug=comic)
        return html_response(comic)


##
# Render a JSON response and send it back.
#
# @param comic Comic model.
# @return HttpResponse
def json_response(comic):
    response_data = {"id": int(comic.pk), "url": settings.SITE['url'] + reverse('comic.views.load_by_slug',
        kwargs={'comic': comic.slug, '_format': 'html'}), "slug": comic.slug, "title": comic.title,
                     "description": comic.description,
                     "author": settings.SITE['url'] + reverse('user.views.load_by_slug',
                         kwargs={'user': comic.author.username, '_format': 'json'}), "panels": [],
                     "created": str(comic.created), "updated": str(comic.updated)}
    for panel in comic.panel_set.all().order_by('sort'):
        response_data['panels'].append(settings.SITE['url'] + panel.source.url)

    next_comic = Comic.objects.filter(pk__gt=comic.id)[:1]
    if next_comic:
        response_data['next'] = settings.SITE['url'] + reverse('comic.views.load_by_slug',
            kwargs={'comic': next_comic[0].slug, '_format': 'json'})

    previous_comic = Comic.objects.filter(pk__lt=comic.id)[:1]
    if previous_comic:
        response_data['previous'] = reverse('comic.views.load_by_slug',
            kwargs={'comic': settings.SITE['url'] + previous_comic[0].slug, '_format': 'json'})

    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")


##
# Render an HTML response and send it back.
#
# @param comic Comic model.
# @return HttpResponse
def html_response(comic):
    next_comic = Comic.objects.filter(pk__gt=comic.id)[:1]
    if next_comic:
        next_comic = next_comic[0]
    else:
        next_comic = False
    previous_comic = Comic.objects.filter(pk__lt=comic.id)[:1]
    if previous_comic:
        previous_comic = previous_comic[0]
    else:
        previous_comic = False
    return render_to_response('comic/item.html',
        {'comic': comic, 'next_comic': next_comic, 'previous_comic': previous_comic})