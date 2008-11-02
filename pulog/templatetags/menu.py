from django import template
from pulog.models import Post

register = template.Library()

@register.inclusion_tag('menu.html', takes_context = True)
def get_menu(context):
    return {
        'menus': Post.objects.get_page(),
        'current': 'current' in context and context['current'],
    }
