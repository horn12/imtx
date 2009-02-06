from django.http import Http404, HttpResponse, HttpResponseRedirect, QueryDict
from django.conf.urls.defaults import *
from django.db.models import Q
from django.template import TemplateDoesNotExist, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.forms.util import ErrorList

from pulog.models import Post, Category, Comment
from pulog.models import Tag, TaggedItem
from pulog.forms import CommentForm
from pulog.views.utils import get_page

def index(request):
    page = get_page(request)

    posts = Post.objects.get_post()
    return render_to_response('post/post_list.html', {
                'posts': posts,
                'page': page,
                }, context_instance = RequestContext(request)
            )

#Dep
def comments_post(request):
    post = Post.objects.filter(id = int(request.POST['post_id']))[0]
    form = CommentForm(request.POST)

    message = ''

    if request.user.is_authenticated():
        if form.data['content']:
            comment = Comment(post = post,
                    author = request.user.get_profile().nickname,
                    email = request.user.email,
                    url = request.user.get_profile().website,
                    IP = request.META['REMOTE_ADDR'],
                    content = form.data['content'],
                    )
            comment.save()
            form = CommentForm()
            return HttpResponseRedirect('%s#comment-%d' % (post.get_absolute_url(), comment.id))
        else:
            form = CommentForm(request.POST)
    else:
        if form.is_valid():
            author = form.cleaned_data['author']
            for user in User.objects.all():
                if author == user.username or author == user.get_profile().nickname:
                    form = CommentForm(request.POST)
                    el = ErrorList()
                    el.append('You can not use the name.')
                    form.errors['author'] = el
                else:
                    if 'ip' in request.COOKIES:
                        message = 'You are posting comments too quickly. Slow down.'
                        return render_to_response('post/error.html',
                                {'message': message}
                                )
                    content = form.cleaned_data['content']
                    email = form.cleaned_data['email']
                    url = form.cleaned_data['url']
                    ip = request.META['REMOTE_ADDR']

                    comment = Comment(post = post,
                            author = author,
                            email = email,
                            url = url,
                            IP = ip,
                            content = content,
                            )
                    comment.save()

                    response = HttpResponseRedirect('/archives/%s.html#comment-%d' % (request.POST['post_id'], comment.id))
                    response.set_cookie('ip',request.META['REMOTE_ADDR'], max_age = 30)
                    response.set_cookie('author', author)
                    response.set_cookie('email', email)
                    response.set_cookie('url', url)

                    return response
        else:
            form = CommentForm(request.POST)

    for field in ['author', 'email', 'content', 'url']:
        if field in form.errors:
            if form.errors[field][0]:
                message = '[%s] %s' % (field.title(), form.errors[field][0].capitalize())
                break

    return render_to_response('post/error.html',
            {'message': message}
            )

def single_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)

    post.view = post.view + 1
    post.save()

    name = None
    if 'name' in request.COOKIES:
        name = request.COOKIES['name']

    email = None
    if 'email' in request.COOKIES:
        email = request.COOKIES['email']

    url = None
    if 'url' in request.COOKIES:
        url = request.COOKIES['url']

    return render_to_response('post/post_detail.html', {
                'post': post,
                'comment_meta': {'name':name, 
                                 'email': email, 
                                 'url': url},
                },
                context_instance = RequestContext(request),
            )

def static_pages(request, page):
    for post in Post.objects.get_page():
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
