# coding: utf-8
import datetime
from django.utils.translation import gettext as _
from django.template import Library
from django.db import connection
from imtx_cn.blog.models import Post, Category, Link, Favourite
from imtx_cn.comments.models import Comment

register = Library()

@register.inclusion_tag('sidebar/recent_posts.html', takes_context = True)
def get_recent_posts(context):
    #TODO Use settings to determine the latest items.
    return {'posts': Post.objects.get_post()[:20]}

@register.inclusion_tag('sidebar/recent_comments.html', takes_context = True)
def get_recent_comments(context):
    comments = Comment.objects.in_public()[:20]

    return {'comments': comments}

@register.inclusion_tag('sidebar/recent_favourites.html', takes_context = True)
def get_recent_favourites(context):
    return {'favourites': Favourite.objects.get_public()[:20]}

@register.inclusion_tag('sidebar/links.html', takes_context = True)
def get_links(context):
    links = Link.objects.all()

    return {'links': links}

@register.inclusion_tag('sidebar/category_list.html', takes_context = True)
def get_categories(context):
    return {'categories': Category.objects.all(),
        'posts': Post.objects.get_post()}

@register.inclusion_tag('sidebar/archive_list.html', takes_context = True)
def get_archive(context):
    return {'months': Post.objects.dates('date', 'month')}
