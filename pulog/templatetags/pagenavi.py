from django import template
from txblog.blog.models import Post

register = template.Library()

@register.tag
def pagenavi(context):
	return {'pages': Post.objects.filter(type = 'page')}
