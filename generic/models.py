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

from django.db import models
from django.contrib.auth.models import User


##
# We're going to store search dumps in a MyISAM table so we can
# do fulltext searches.
class Search(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    model = models.CharField(max_length=32)
    model_id = models.IntegerField(max_length=16)
    url = models.CharField(max_length=255)
    created = models.DateTimeField('date created', auto_now_add=True)
    updated = models.DateTimeField('date updated', auto_now=True)


##
# Let's store our bio in MySQL so we can edit it via the admin.
class About(models.Model):
    user_id = models.ForeignKey(User)
    content = models.TextField()
    avatar = models.FileField(upload_to='generic/about/%id')
    created = models.DateTimeField('date created', auto_now_add=True)
    updated = models.DateTimeField('date updated', auto_now=True)


# We're going to use these for the Rewrite choices.
REQUEST_METHODS = (
    ('GET', 'GET'),
    ('POST', 'POST'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE'),
)


##
# If I want to move comics/users/whatever to a new location, this will help with that.
class Rewrite(models.Model):
    request_method = models.CharField(max_length=1, choices=REQUEST_METHODS)
    request_uri = models.CharField(max_length=255)
