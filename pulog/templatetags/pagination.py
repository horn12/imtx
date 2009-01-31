from django import template
from django.core.paginator import Paginator, InvalidPage

register = template.Library()

OBJECTS_PER_PAGE = 8

def get_page_range(current, range):
    if range[-1] < 8:
        return xrange(1, range[-1] + 1)

    if range[-1] - current < 4:
        first = range[-1] - 7
    elif current > 4:
        first = current - 3
    else:
        first = 1

    if first + 7 < range[-1]:
        last = first + 8
    else:
        last = range[-1] + 1
        
    return xrange(first, last)

class PaginationNode(template.Node):
    def __init__(self, objects, page):
        self.object_var_name = objects 
        self.objects_to_be_paginated = template.Variable(objects)
        self.current_page = template.Variable(page)

    def render(self, context):
        objects = self.objects_to_be_paginated.resolve(context)
        current = int(self.current_page.resolve(context))
        pagi = Paginator(objects, OBJECTS_PER_PAGE)
        page = pagi.page(current)

        context[self.object_var_name] = page.object_list
        context['pagi_page'] = page
        context['pagi_current'] = current
        context['pagi_range'] = get_page_range(current, pagi.page_range)
        return ''

@register.tag
def pre_pagination(parser, token):
    tag_name, objects, page = token.split_contents()

    return PaginationNode(objects, page)
	
@register.inclusion_tag('pagination.html', takes_context = True)
def do_pagination(context):
    if 'pagi_path' in context:
        pagi_path = context['pagi_path']
    else:
        pagi_path = ''
    return {
            'pagi_page': context['pagi_page'],
            'pagi_current': context['pagi_current'],
            'pagi_range': context['pagi_range'],
            'pagi_path': pagi_path,
            }
