from django import template
from imtx_cn.blog.models import Page

register = template.Library()

@register.inclusion_tag('menu.html', takes_context = True)
def get_menu(context):
    return {
        'menus': Page.objects.get_page(),
        'current': 'current' in context and context['current'],
    }
