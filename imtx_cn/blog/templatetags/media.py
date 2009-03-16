import re
from django import template
from imtx_cn.blog.models import Media

register = template.Library()

class MediaNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = Media.objects.all().order_by('-date')[:10]
        return ''

@register.tag
def get_media(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'^as (\w+)', args)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    var_name, = m.groups()
    return MediaNode(var_name)

@register.inclusion_tag('menu.html', takes_context = True)
def get_menu(context):
    return {
        'menus': Post.objects.get_page(),
        'current': 'current' in context and context['current'],
    }
