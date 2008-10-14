from django import template
from pulog.models import Post

register = template.Library()

@register.tag
def list_pages(context):
	return {'pages': Post.objects.filter(type = 'page')}


