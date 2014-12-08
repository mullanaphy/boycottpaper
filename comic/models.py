# -*- coding: utf-8 -*-
import re
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from generic.models import Search


# Main comic model, it houses our comics main details and links to all
# of its panels.
class Comic(models.Model):
    author = models.ForeignKey(User)
    slug = models.SlugField(max_length=32)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    cover = models.FileField(upload_to='comic/%y/%m/%d/%cover')
    created = models.DateTimeField('date created', auto_now_add=True)
    updated = models.DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return self.title


# Our comics are made up of one to four images, each panel is separate
# in order to dynamically change the page layout depending on our end
# user's resolution.
class Panel(models.Model):
    comic = models.ForeignKey(Comic)
    alt = models.CharField(max_length=255)
    source = models.FileField(upload_to='comic/%y/%m/%d/%id')
    sort = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.comic) + ' » Panel #' + str(self.sort)


# On Comic save we're going to dump all of its alphanumeric content
# into a Search model, which has a full text index. This way we can
# do a match against for search instead of something like Sphinx
# since as of right now that would be overkill for a simple comic
# website.
@receiver(post_save, sender=Comic)
def on_comic_save_update_search_data(sender, instance, **kwargs):
    try:
        search = Search.objects.get(model='comic', model_id=instance.id)
    except Search.DoesNotExist:
        search = Search(model='Comic', model_id=instance.id)
        pass

    # Add all of our content into Search, including al text from all
    # of the panels.
    content = instance.title + ' ' + instance.description
    content = content.lower()
    for panel in instance.panel_set.all():
        content += ' ' + panel.alt
    search.content = re.sub(r'[^a-zA-Z0-9 ]+', '', content)

    search.title = instance.title
    search.description = instance.description

    # Make our url.
    search.url = reverse('comic.views.load_by_slug', kwargs={'comic': instance.slug, '_format': 'html'})

    # And save it.
    search.save()


# On Panel save we should look to update our Comic's search model.
@receiver(post_save, sender=Panel)
def on_panel_save_update_search_data(sender, instance, **kwargs):
    return on_comic_save_update_search_data(sender, instance.comic, **kwargs)
