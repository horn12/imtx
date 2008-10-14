import os
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from pulog.models import Post, Category

post_info = {
		'queryset': Post.objects.filter(type = 'post').order_by('-date'),
		}

urlpatterns = patterns('',
		(r'^(?P<object_id>\d+)/comment/$', 'django.views.generic.list_detail.object_detail',
		dict(post_info, template_name = 'post/comment_ajax.html')),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), 'static')}),
)

urlpatterns += patterns('pulog.views',
		(r'^$', 'index'),
		(r'^(?P<post_id>\d+).html$', 'single_post'),
        (r'^category/(?P<slugname>[^/]+)$', 'category_view'),
        (r'^category/(?P<slugname>[^/]+)/page/(?P<page_num>\d+)$', 'category_view'),
        (r'^(?P<year>\d{4})/(?P<month>\d{1,2})$', 'archive_view'),
        (r'^(?P<year>\d{4})/(?P<month>[^/]+)/page/(?P<page_num>\d+)$', 'archive_view'),
#        (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page_num>\d+)$', 'archive_view'),
)
