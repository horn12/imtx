from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render_to_response, get_object_or_404
from models import Tag
from models import TaggedItem
from imtx.apps.blog.models import Post
from imtx.apps.pagination.utils import get_page

def tag_view(request, slug):
    tag = get_object_or_404(Tag, slug = slug)
    posts = TaggedItem.objects.get_by_model(Post, tag).order_by('-date')
    page = get_page(request)

    return render_to_response('tag/tag.html', {
                'tag': tag, 
                'posts': posts,
                'page': page,
                'pagi_path': request.path
                }, context_instance = RequestContext(request)
            )
