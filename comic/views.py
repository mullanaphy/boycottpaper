from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import json as simplejson
import random as randomint
from comic.models import Comic

# Load an index page listing all of our comics.
def index(request):
    collection = Comic.objects.all().order_by('-created')[:25]
    t = loader.get_template('comic/collection.html')
    c = Context({
        'collection': collection,
    })
    return HttpResponse(t.render(c))

# Return my first comic ever.
def first(request):
    comic = Comic.objects.all().order_by('created')[0]
    return redirect('comic.views.load_by_slug', comic = comic.slug, _format = 'html')

# Return the latest comic.
def latest(request):
    comic = Comic.objects.all().order_by('-created')[0]
    return redirect('comic.views.load_by_slug', comic = comic.slug, _format = 'html')

# Return all popular comics.
def popular(popular):
    comic_list = Comic.objects.all().order_by('-karma')[:25]
    t = loader.get_template('comic/collection.html')
    c = Context({
        'comic_list': comic_list,
    })
    return HttpResponse(t.render(c))

# Randomly select a comic and then redirect to its canonical url.
def random(request):
    count = Comic.objects.all().count()
    i = randomint.random() * count + 1
    comic = Comic.objects.get(pk = i)
    return redirect('comic.views.load_by_slug', comic = comic.slug, _format = 'html')

# Load by a pk
def load_by_pk(request, comic, _format = 'html'):
    if _format == 'json':
        try:
            comic = Comic.objects.get(pk = comic)
            return json_response(comic)
        except Comic.DoesNotExist as e:
            return HttpResponse(simplejson.dumps({
                "error": str(e),
            }), mimetype = "application/json", status = 404)
            pass
    else:
        comic = get_object_or_404(Comic, pk = comic)
        return html_response(comic)

# Load by a slug
def load_by_slug(request, comic, _format = 'html'):
    if _format == 'json':
        try:
            comic = Comic.objects.get(slug = comic)
            return json_response(comic)
        except Comic.DoesNotExist as e:
            return HttpResponse(simplejson.dumps({
                "error": str(e),
            }), mimetype = "application/json", status = 404)
            pass
    else:
        comic = get_object_or_404(Comic, slug = comic)
        return html_response(comic)

# Load a comic in json form.
def json_response(comic):
    response_data = {
        "id": int(comic.pk),
        "url": settings.SITE['url'] + reverse('comic.views.load_by_slug',
            kwargs = {'comic': comic.slug, '_format': 'html'}),
        "slug": comic.slug,
        "title": comic.title,
        "description": comic.description,
        "author": settings.SITE['url'] + reverse('user.views.load_by_slug',
            kwargs = {'user': comic.author.username, '_format': 'json'}),
        "panels": [],
        "created": str(comic.created),
        "updated": str(comic.updated)
    }
    for panel in comic.panel_set.all().order_by('sort'):
        response_data['panels'].append(settings.SITE['url'] + panel.source.url)
    return HttpResponse(simplejson.dumps(response_data), mimetype = "application/json")

# Return an HTML Response.
def html_response(comic):
    return render_to_response('comic/item.html', {'comic': comic})