from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.http import HttpResponse
from django import template
from django.template import Library
from django.db import connection
from pulog.models import Post, Category, Comment, Link

register = Library()

class CountNode(template.Node):
    def __init__(self, property, nonecase, singular, plural):
        self.property = property
        self.nonecase = nonecase
        self.singular = singular
        self.plural = plural

    def render(self, context):
        count = getattr(context['post'], 'get_%s_count' % self.property)()
        if count:
            countinfo = ngettext(self.singular, self.plural, count)
            if count == 1:
                return countinfo
        else:
            return self.nonecase

        return countinfo % {'count': count}

@register.tag(name="get_comments_count")
def do_comments_count(parser, token):
    return CountNode("comments", _("No Comments"),  _("One Comment"), _("%(count)d Comments"))

@register.tag(name="get_views_count")
def do_views_count(parser, token):
    return CountNode("views", _("No Views"), _("One View"), _("%(count)d Views"))
