from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render_to_response, get_object_or_404
from pulog.models import Tag
from pulog.models import Post
from pulog.models import TaggedItem
from pulog.views.utils import get_page_and_query

def tag_view(request, slug):
    tag = get_object_or_404(Tag, slug = slug)
    posts = TaggedItem.objects.get_by_model(Post, tag).order_by('-date')
    page, query = get_page_and_query(request)

    return render_to_response('tag/tag.html', {
                'tag': tag, 
                'posts': posts,
                'page': page,
                'pagi_path': request.path
                }, context_instance = RequestContext(request)
            )
