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

from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import json as simplejson
from collections import OrderedDict


##
# Our main user collection. This will return 5 users.
#
# @param request HttpRequest coming in from Django.
# @return HttpResponse
# @TODO Add pagination. Not really important unless I actually get donations.
def index(request):
    collection = User.objects.all().order_by('-created')[:5]
    t = loader.get_template('user/collection.html')
    c = Context({'collection': collection, 'path': request.path})
    return HttpResponse(t.render(c))


##
# Load a user by their user_id.
#
# @param request HttpRequest coming in from Django.
# @param user User's user_id.
# @param _format File format to use, either html or json.
# @return HttpResponse
def load_by_pk(request, user, _format='html'):
    if _format == 'json':
        try:
            user = get_object_or_404(User, pk=user)
            return json_response(user)
        except User.DoesNotExist as e:
            return HttpResponse(simplejson.dumps({"error": str(e), }), mimetype="application/json", status=404)
            pass
    else:
        user = get_object_or_404(User, pk=user)
        return html_response(user, request)


##
# Load a user by their username.
#
# @param request HttpRequest coming in from Django.
# @param user User's username.
# @param _format File format to use, either html or json.
# @return HttpResponse
def load_by_slug(request, user, _format='html'):
    if _format == 'json':
        try:
            user = get_object_or_404(User, username=user)
            return json_response(user)
        except User.DoesNotExist as e:
            return HttpResponse(simplejson.dumps({"error": str(e), }), mimetype="application/json", status=404)
            pass
    else:
        user = get_object_or_404(User, username=user)
        return html_response(user, request)


##
# Send a JSON response back.
#
# @param user User model.
# @return HttpResponse
def json_response(user):
    response_data = OrderedDict([
        ("id", int(user.pk)),
        ("username", user.username),
        ("fullname", user.first_name + " " + user.last_name),
        ("bio", user.about_set.all()[:1][0].content),
        ("email", user.email),
        ("comics", []),
        ("created", str(user.date_joined)),
        ("updated", str(user.last_login))
    ])
    for comic in user.comic_set.all().order_by('-pk')[:5]:
        response_data['comics'].append(
            settings.SITE['url'] + reverse('comic.views.load_by_slug', kwargs={
                'comic': comic.slug,
                '_format': 'json'
            })
        )
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")


##
# Send an HTML response back.
#
# @param user User model.
# @param request HttpRequest coming in from Django.
# @return HttpResponse
def html_response(user, request):
    return render_to_response('user/item.html', {
        'user': user,
        'path': request.path
    })
