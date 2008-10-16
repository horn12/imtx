import os
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from pulog.models import Post, Category
from pulog.feed import LatestPosts

from django.contrib import admin
admin.autodiscover()

post_info = {
    'queryset': Post.objects.filter(type = 'post').order_by('-date'),
}

feed = {
    'latest': LatestPosts,
}

urlpatterns = patterns('',
        (r'^admin/(.*)', admin.site.root),
        (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', 
            {'feed_dict': feed}),
        (r'^(?P<object_id>\d+)/comment/$', 
            'django.views.generic.list_detail.object_detail', 
            dict(post_info, template_name = 'ImTX/post/comment_ajax.html')),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), 'static')}),
        (r'^templates/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), 'templates')}),
)

urlpatterns += patterns('pulog.views',
        (r'^$', 'index'),
        (r'^archives/$', 'index'),
        (r'^archives/(?P<post_id>\d+).html$', 'single_post'),
        (r'^archives/category/(?P<slugname>[^/]+)$', 'category_view'),
        (r'^archives/category/(?P<slugname>[^/]+)/page/(?P<page_num>\d+)$', 'category_view'),
        (r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})$', 'archive_view'),
        (r'^archives/(?P<year>\d{4})/(?P<month>[^/]+)/page/(?P<page_num>\d+)$', 'archive_view'),
        (r'^commentspost/$', 'comments_post'),
        (r'^page/(?P<num>\d+)', 'page'),
        (r'(\w+)$', 'static_pages'),
#        (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page_num>\d+)$', 'archive_view'),
)
