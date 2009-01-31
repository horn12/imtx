from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render_to_response, get_object_or_404
from pulog.models import Tag
from pulog.models import Post
from pulog.models import TaggedItem

def tag_view(request, slug, page_num = None):
    tag = get_object_or_404(Tag, slug = slug)
    posts = TaggedItem.objects.get_by_model(Post, tag).order_by('-date')

    if page_num:
        current_page = int(page_num)
    else:
        current_page = 1
    
    link = '/archives/tag/%s' % slug

    page = None
    range = None
    if len(posts) > 5:
        pagi = Paginator(posts, 5)
        range = get_page_range(current_page, pagi.page_range)
        page = pagi.page(current_page)
        posts = page.object_list

    return render_to_response('tag/tag.html', 
                {'tag': tag, 
                'posts': posts,
                'page': page,
                'current_page': current_page,
                'range': range,
                'link': link},
                context_instance = RequestContext(request)
                )
