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


##
# Generic index page, have some meta data related to our comic.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def index(request):
    collection = Comic.objects.all().order_by('-created')[:3]
    t = loader.get_template('generic/collection.html')
    c = Context({'collection': collection, })
    return HttpResponse(t.render(c))


##
# Search our comics. Theoretically this could search other models as well since
# it only searches the Search model, so other data could be entered there.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def search(request):
    if request.REQUEST['q']:
        search = Search.objects.all().filter(content__contains=request.REQUEST['q'].lower())
        t = loader.get_template('generic/search/results.html')
        c = Context({'q': request.REQUEST['q'], 'collection': search, })
        return HttpResponse(t.render(c))
    else:
        return render_to_response('generic/search/results.html')


##
# Show the about me for the first User. Ideally you might want to change this
# to load user bios based on a user's group.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def about(request):
    about = get_object_or_404(About, pk=1)
    return render_to_response('generic/about.html', {'about': about})
