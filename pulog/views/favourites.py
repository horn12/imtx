from django.http import Http404, HttpResponse, HttpResponseRedirect, QueryDict
from django.core.paginator import Paginator, InvalidPage
from django.conf.urls.defaults import *
from django.db.models import Q
from django.template import TemplateDoesNotExist, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.utils import encoding, html
from pulog.models import Favourite
from pulog.views.utils import get_page
from pulog.views.comment import get_comment_cookie_meta

def index(request):
    favourites = Favourite.objects.get_public()
    page = get_page(request)

    return render_to_response('favourites/favourite_list.html', {
                    'page': page,
                    'favourites': favourites,
                    'pagi_path': request.path,
                    'current': 'favourites',
                    }, context_instance = RequestContext(request)
                )

def single(request, id):
    favourite = get_object_or_404(Favourite, id = id)

    if favourite:
        favourite.view = favourite.view + 1
        favourite.save()

        return render_to_response('favourites/favourite_detail.html', {
                      'favourite': favourite,
                      'current': 'favourites',
                      'comment_meta': get_comment_cookie_meta(request),
                      },
                context_instance = RequestContext(request),
                )
    else:
        return Http404
