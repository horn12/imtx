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
from pulog.utils import get_page_range

def index(request):
    favourites = Favourite.objects.get_public()

    if len(favourites) > 5:
        pagi = Paginator(favourites, 5)
        page = pagi.page(1)
        current_page = 1
        favourites = page.object_list
        range = get_page_range(current_page, pagi.page_range)
    else:
        page = None
        current_page = None
        first, last = None, None
        range = None

    return render_to_response('favourites/favourite_list.html', 
                {'page': page,
                'favourites': favourites,
                'range': range,
                'current_page': current_page},
                context_instance = RequestContext(request)
                )

def single(request, id):
    favourite = get_object_or_404(Favourite, id = id)

    if favourite:
        favourite.view = favourite.view + 1
        favourite.save()

        return render_to_response('favourites/favourite_detail.html', {'favourite': favourite},
                context_instance = RequestContext(request),
                )
    else:
        return Http404
