# coding: utf-8
import datetime
from django.utils.translation import gettext as _
from django.template import Library
from django.db import connection
from pulog.models import Post, Category, Comment, Link

register = Library()

@register.inclusion_tag('sidebar/recent_posts.html', takes_context = True)
def get_recent_posts(context):
    return {'posts': Post.objects.get_post()[:10]}

@register.inclusion_tag('sidebar/recent_comments.html', takes_context = True)
def get_recent_comments(context):
    comments = Comment.objects.in_public()[:10]

    return {'comments': comments}

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
