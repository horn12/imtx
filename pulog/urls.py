import os
from django.contrib import admin
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from settings import MEDIA_ROOT, TEMPLATE_ROOT
from pulog.models import Post, Category
from pulog.feed import LatestPosts
admin.autodiscover()

post_info = {
    'queryset': Post.manager.get_post(),
}

feed = {
    'latest': LatestPosts,
}

urlpatterns = patterns('',
        (r'^admin/(.*)', admin.site.root),
        (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', 
            {'feed_dict': feed}),
        (r'^templates/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': TEMPLATE_ROOT}),
#        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
#            {'document_root': MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'dynamic_media_serve.serve', 
            {'document_root': MEDIA_ROOT}),
)

urlpatterns += patterns('pulog.views',
        (r'^$', 'index'),
        (r'^archives/$', 'index'),
        (r'^archives/(?P<post_id>\d+).html$', 'single_post'),
        (r'^archives/category/(?P<slugname>[^/]+)/$', 'category_view'),
        (r'^archives/category/(?P<slugname>[^/]+)/page/(?P<page_num>\d+)/$', 
            'category_view'),
        (r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive_view'),
        (r'^archives/(?P<year>\d{4})/(?P<month>[^/]+)/page/(?P<page_num>\d+)/$',
            'archive_view'),
        (r'^commentspost/$', 'comments_post'),
        (r'^page/(?P<num>\d+)/$', 'page'),
        (r'(\w+)$', 'static_pages'),
#        (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page_num>\d+)$', 'archive_view'),
)
