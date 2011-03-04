from django import template
from imtx.apps.blog.models import Menu

register = template.Library()

@register.inclusion_tag('menu.html', takes_context=True)
def get_menu(context):
    return {
        'menus': Menu.objects.get_root_menu(),
        'current': 'current' in context and context['current'],
    }
