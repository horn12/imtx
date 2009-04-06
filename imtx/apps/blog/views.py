from django.http import Http404, HttpResponseRedirect, QueryDict
from django.conf.urls.defaults import *
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.utils import html
from django.core import urlresolvers

from models import Post, Page, Category
from forms import MediaForm
from imtx.apps.tagging.models import Tag
from imtx.apps.comments.views import get_comment_cookie_meta
from imtx.apps.pagination.utils import get_page

def get_query(request):
    query = html.escape(request.GET.get('s', ''))
    return query

def index(request):
    page = get_page(request)

    posts = Post.objects.get_post()
    return render_to_response('post/post_list.html', {
                'posts': posts,
                'page': page,
                }, context_instance = RequestContext(request)
            )

def single_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)

    post.hit_views()

    return render_to_response('post/post_detail.html', {
                'post': post,
                'comment_meta': get_comment_cookie_meta(request),
                },
                context_instance = RequestContext(request),
            )

def static_pages(request, page):
    for post in Page.objects.get_page():
        try:
            if post.slug == page:
                return render_to_response('post/page.html', 
                        {'post': post, 'current': post.slug},
                            context_instance = RequestContext(request),
                        )
        except TypeError:
            raise Http404

    raise Http404

def category_view(request, slug):
    cat = get_object_or_404(Category, slug = slug)
    posts = Post.objects.get_post_by_category(cat)
    page = get_page(request)

    return render_to_response('post/archive.html', {
                'category': cat, 
                'posts': posts,
                'path': request.path,
                'page': page,
                }, context_instance = RequestContext(request)
            )

def archive_view(request, year, month):
    posts = Post.objects.get_post_by_date(year, month)
    page = get_page(request)
    
    return render_to_response('post/archive.html', {
                'year': year,
                'month': month,
                'posts': posts,
                'path': request.path,
                'page': page,
                }, context_instance = RequestContext(request)
            )

def search(request):
    query = get_query(request)
    page = get_page(request)

    qd = request.GET.copy()
    if 'page' in qd:
        qd.pop('page')

    posts = None

    if query:
        if 'search' in request.COOKIES:
            message = 'You are searching too often. Slow down.'
            return render_to_response('post/error.html',
                    {'message': message}
                    )
        qset = (
            Q(title__icontains = query) |
            Q(content__icontains = query)
        )

        posts = Post.objects.filter(qset, status = 'publish').distinct().order_by('-date')

    response = render_to_response('search.html', {
                              'query': query,
                              'posts': posts,
                              'page': page,
                              'pagi_path': qd.urlencode(),
                              })
    response.set_cookie('search',request.META['REMOTE_ADDR'], max_age = 5)

    return response

def redirect_feed(request):
    return HttpResponseRedirect(urlresolvers.reverse('feed', args=('latest',)))

def upload(request):
    #FIXME Use auth
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            new_object = form.save(commit = False)
            new_object.save()
            form.clean()
    else:
        form = MediaForm()
    return render_to_response('utils/upload.html', {'form': form})

from datetime import time, date, datetime
from time import strptime

from pingback import create_ping_func
from django_xmlrpc import xmlrpcdispatcher

# create simple function which returns Post object and accepts
# exactly same arguments as 'details' view.
def pingback_post_handler(post_id, **kwargs):
    return Post.objects.get(id=post_id)

def pingback_page_handler(page, **kwargs):
    return Page.objects.get(slug=page)

# define association between view name and our handler
ping_details = {
    'single_post': pingback_post_handler,
    'static_pages': pingback_page_handler,
}

# create xml rpc method, which will process all
# ping requests
ping_func = create_ping_func(**ping_details)

# register this method in the dispatcher
xmlrpcdispatcher.register_function(ping_func, 'pingback.ping')
