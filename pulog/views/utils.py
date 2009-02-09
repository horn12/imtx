"""
A few bits of helper functions for comment views.
"""

import urllib
import textwrap
from django.http import HttpResponseRedirect
from django.core import urlresolvers
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.utils import html
from django.db.models import Q
from django.conf import settings
from pulog.models import Tag
from pulog.models import Post
from pulog.models import Comment
from pulog.models import Media
from pulog.forms import MediaForm

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

def break_lines(request):
    from pulog.models import Post
    from pulog.utils import new_linebreaks
    for p in Post.objects.all():
#        p.content = new_linebreaks(p.content)
#        p.content = p.content.replace('http://imtx.cn/wp-content', 'http://imtx.cn/static/uploads')
        p.tag = ','.join([t.name for t in Tag.objects.get_for_object(p)])

        p.save()

    return HttpResponseRedirect('/')

def redirect_feed(request):
    return HttpResponseRedirect(urlresolvers.reverse('feed', args=('latest',)))

def get_page(request):
    page = request.GET.get('page', '')
    if not page:
        page = 1
    return page

def get_query(request):
    query = html.escape(request.GET.get('s', ''))
    return query

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

def next_redirect(data, default, default_view, **get_kwargs):
    """
    Handle the "where should I go next?" part of comment views.

    The next value could be a kwarg to the function (``default``), or a
    ``?next=...`` GET arg, or the URL of a given view (``default_view``). See
    the view modules for examples.

    Returns an ``HttpResponseRedirect``.
    """
    next = data.get("next", default)
    if next is None:
        next = urlresolvers.reverse(default_view)
    if get_kwargs:
        next += "?" + urllib.urlencode(get_kwargs)
    return HttpResponseRedirect(next)

def confirmation_view(template, doc="Display a confirmation view."):
    """
    Confirmation view generator for the "comment was
    posted/flagged/deleted/approved" views.
    """
    def confirmed(request):
        comment = None
        if 'c' in request.GET:
            try:
                comment = Comment.objects.get(pk=request.GET['c'])
            except ObjectDoesNotExist:
                pass
        return render_to_response(template,
            {'comment': comment},
            context_instance=RequestContext(request)
        )

    confirmed.__doc__ = textwrap.dedent("""\
        %s

        Templates: `%s``
        Context:
            comment
                The posted comment
        """ % (doc, template)
    )
    return confirmed
