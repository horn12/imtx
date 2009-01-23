from django import http
from django.conf import settings
from utils import next_redirect, confirmation_view
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.http import require_POST
from pulog.forms import CommentForm
from pulog import signals

class CommentPostBadRequest(http.HttpResponseBadRequest):
    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """
    def __init__(self, why):
        super(CommentPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string("comment/400-debug.html", {"why": why})

@require_POST
def post_comment(request, next = None):
    """
    Post a comment.

    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comment/preview.html``, will be rendered.
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    if request.user.is_authenticated():
        if not data.get('name', ''):
            try:
                data['name'] = request.user.get_profile().nickname
            except:
                data['name'] = request.user.get_full_name() or request.user.username
        if not data.get('email', ''):
            data["email"] = request.user.email
        if not data.get('url', ''):
            try:
                data['url'] = request.user.get_profile().website
            except:
                data['url'] = ''

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        return CommentPostBadRequest("Missing content_type or object_pk field.")
    try:
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.get(pk=object_pk)
    except TypeError:
        return CommentPostBadRequest(
            "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return CommentPostBadRequest(
            "The given content-type %r does not resolve to a valid model." % \
                escape(ctype))
    except ObjectDoesNotExist:
        return CommentPostBadRequest(
            "No object matching content-type %r and object PK %r exists." % \
                (escape(ctype), escape(object_pk)))

    # Construct the comment form
    form = CommentForm(target, data=data)

    # Check security information
    if form.security_errors():
        return CommentPostBadRequest(
            "The comment form failed security verification: %s" % \
                escape(str(form.security_errors())))

    # If there are errors
    if form.errors:
        for field in ['author', 'email', 'content', 'url']:
            if field in form.errors:                                              
                if form.errors[field][0]:                                         
                    message = '[%s] %s' % (field.title(), form.errors[field][0].capitalize())
                    break

        return render_to_response('post/error.html', {'message': message})

    # Otherwise create the comment
    comment = form.get_comment_object()
    comment.parent_id = data['parent_id']
    comment.ip_address = request.META.get("REMOTE_ADDR", None)
    if request.user.is_authenticated():
        comment.user = request.user

    # Signal that the comment is about to be saved
    responses = signals.comment_will_be_posted.send(
        sender  = comment.__class__,
        comment = comment,
        request = request
    )

    for (receiver, response) in responses:
        if response == False:
            return CommentPostBadRequest(
                "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

    # Save the comment and signal that it was saved
    comment.save()
    signals.comment_was_posted.send(
        sender  = comment.__class__,
        comment = comment,
        request = request
    )

    response = HttpResponseRedirect('%s#comment-%d' % (target.get_absolute_url(), comment.id))
    response.set_cookie('ip', comment.ip_address, max_age = 30)
    response.set_cookie('author', comment.user_name)
    response.set_cookie('email', comment.user_email)
    response.set_cookie('url', comment.user_url)

    return response

    return next_redirect(data, next, comment_done, c=comment._get_pk_val())

comment_done = confirmation_view(
    template = "comment/posted.html",
    doc = """Display a "comment was posted" success page."""
)
