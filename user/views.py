from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import json as simplejson

# Create your views here.
def index(request):
    collection = User.objects.all().order_by('-created')[:25]
    t = loader.get_template('user/collection.html')
    c = Context({
        'collection': collection,
    })
    return HttpResponse(t.render(c))

# Load by a pk
def load_by_pk(request, user, _format = 'html'):
    if _format == 'json':
        try:
            user = User.objects.get(pk = user)
            return HttpResponse(simplejson.dumps(request.META.get('HTTP_ACCEPT')), mimetype = "application/json")
        except User.DoesNotExist as e:
            return HttpResponse(simplejson.dumps({
                "error": str(e),
            }), mimetype = "application/json", status = 404)
            pass
    else:
        user = get_object_or_404(User, pk = user)
        return html_response(user)

# Load by a slug
def load_by_slug(request, user, _format = 'html'):
    if _format == 'json':
        try:
            user = User.objects.get(username = user)
            return json_response(user)
        except User.DoesNotExist as e:
            return HttpResponse(simplejson.dumps({
                "error": str(e),
            }), mimetype = "application/json", status = 404)
            pass
    else:
        user = get_object_or_404(User, username = user)
        return html_response(user)

# Load a user in json form.
def json_response(user):
    response_data = {
        "id": int(user.pk),
        "username": user.username,
        "fullname": user.first_name + " " + user.last_name,
        "bio": user.about_set.all()[:1][0].content,
        "email": user.email,
        "comics": [],
        "created": str(user.date_joined),
        "updated": str(user.last_login)
    }
    for comic in user.comic_set.all().order_by('-pk')[:5]:
        response_data['comics'].append(settings.SITE['url'] + reverse('comic.views.load_by_slug',
            kwargs = {'comic': comic.slug, '_format': 'html'}))
    return HttpResponse(simplejson.dumps(response_data), mimetype = "application/json")

# Return an HTML Response.
def html_response(user):
    return render_to_response('user/item.html', {'user': user})

