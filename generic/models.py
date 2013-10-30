from django.db import models
from django.contrib.auth.models import User

# We're going to store search dumps in a MyISAM table so we can
# do fulltext searches.
class Search(models.Model):
    content = models.TextField()
    title = models.CharField(max_length = 32)
    description = models.CharField(max_length = 255)
    model = models.CharField(max_length = 32)
    model_id = models.IntegerField(max_length = 16)
    url = models.CharField(max_length = 255)
    created = models.DateTimeField('date created', auto_now_add = True)
    updated = models.DateTimeField('date updated', auto_now = True)

# Let's store our bio in MySQL so we can edit it via the admin.
class About(models.Model):
    user_id = models.ForeignKey(User)
    content = models.TextField()
    avatar = models.FileField(upload_to = 'generic/about/%id')
    created = models.DateTimeField('date created', auto_now_add = True)
    updated = models.DateTimeField('date updated', auto_now = True)
