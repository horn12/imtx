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
from django.conf import settings
from pulog.models import Comment
from pulog.models import Media
from pulog.forms import MediaForm

def break_lines(request):
    from pulog.models import Post
    from pulog.utils import new_linebreaks
    for p in Post.objects.all():
        p.content = new_linebreaks(p.content)
#        p.content = p.content.replace('http://imtx.cn/wp-content', 'http://ldcn.org/static/uploads')
        p.save()

    return HttpResponseRedirect('/')

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
