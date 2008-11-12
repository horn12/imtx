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

class MonthArchive:
    title = ""
    link = ""
    year = 0
    month = 0

    def __init__(self, month):
        date = month.split("-")
        self.year = int(date[0])
        self.month = int(date[1])
        
        self.title = datetime.date(self.year, self.month, 1).strftime(_('%B %Y'))
        self.link = '/archives/%s/%s/' % (date[0], date[1])

    def get_post_count(self):
        return Post.objects.get_post_by_date(self.year, self.month).count()

@register.inclusion_tag('sidebar/archive_list.html', takes_context = True)
def get_archive(context):
    months = []
    archive_months = []

    for post in Post.objects.all():
        month = post.date.date().strftime('%Y-%m')
        if month not in months:
            months.append(month)

    for month in months:
        archive_months.insert(0, MonthArchive(month))

    return {'months': archive_months}
