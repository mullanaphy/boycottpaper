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
from django.shortcuts import render_to_response, get_object_or_404
from comic.models import Comic
from generic.models import Search, About
from django.http import HttpResponse
from comic.views import html_response as comic_html_response
import markdown


##
# Generic index page, have some meta data related to our comic.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def index(request):
    comic = Comic.objects.all().order_by('-id')[:1]
    if comic:
        comic = comic[0]
        return comic_html_response(comic, request)

    return render_to_response('generic/index.html', {'path': request.path})


##
# Search our comics. Theoretically this could search other models as well since
# it only searches the Search model, so other data could be entered there.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def search(request):
    if 'q' in request.REQUEST:
        collection = find(request.REQUEST['q'].lower())
        t = loader.get_template('generic/search/results.html')
        c = Context({'q': request.REQUEST['q'], 'collection': collection})
        return HttpResponse(t.render(c))
    else:
        return render_to_response('generic/search/results.html', {'path': request.path})


##
# Show the about me for the first User. Ideally you might want to change this
# to load user bios based on a user's group.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def about(request):
    about = get_object_or_404(About, pk=1)
    return render_to_response('generic/about.html', {'content': markdown.markdown(about.content), 'path': request.path})


##
# Render our 400 error pages.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def error400(request):
    return error(400, request)


##
# Render our 403 error pages.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def error403(request):
    return error(403, request)


##
# Render our 404 error pages.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def error404(request):
    t = loader.get_template('generic/error/404.html')
    collection = find(request.path.replace('/', ''))
    return HttpResponse(t.render(Context({'error': 404, 'path': request.path, 'collection': collection})), status=404)


##
# Render our 500 error pages.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def error500(request):
    return error(500, request)


##
# Actually render our error pages.
#
# @param int status_code
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def error(status_code, request):
    t = loader.get_template('generic/error/' + str(status_code) + '.html')
    return HttpResponse(t.render(Context({'error': status_code, 'path': request.path})), status=status_code)


def find(term):
    return Search.objects.all().filter(content__contains=term)
