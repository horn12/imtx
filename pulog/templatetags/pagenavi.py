from django import template
from pulog.models import Post

register = template.Library()

@register.tag
def pagenavi(context):
	return {'pages': Post.manager.get_page()}
