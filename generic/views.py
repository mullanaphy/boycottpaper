from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from comic.models import Comic
from generic.models import Search, About
from django.http import HttpResponse

# Generic index page, have some meta data related to our comic.
def index(request):
    latest_comic_list = Comic.objects.all().order_by('-created')[:5]
    t = loader.get_template('generic/index.html')
    c = Context({'latest_comic_list': latest_comic_list, })
    return HttpResponse(t.render(c))


# Search our comics, blogs, and maybe about me?
def search(request):
    if request.REQUEST['q']:
        search = Search.objects.all().filter(content__contains=request.REQUEST['q'].lower())
        t = loader.get_template('generic/search/results.html')
        c = Context({'q': request.REQUEST['q'], 'collection': search, })
        return HttpResponse(t.render(c))
    else:
        return render_to_response('generic/search/form.html')


# See an about me page.
def about(request):
    about = get_object_or_404(About, pk=1)
    return render_to_response('generic/about.html', {'about': about})
