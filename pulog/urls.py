import os
from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page

from pulog.models import Post, Category
from pulog.feed import LatestPosts

admin.autodiscover()

class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Post.objects.get_page()

    def lastmod(self, obj):
        return obj.date

class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.2

    def items(self):
        return Post.objects.get_post()

    def lastmod(self, obj):
        return obj.date

sitemaps = {
    'posts': PostSitemap,
    'pages': PageSitemap,
}

feed = {
    'latest': LatestPosts,
}

urlpatterns = patterns('',
#        (r'linebreak/', 'pulog.views.utils.break_lines'),
        (r'^sitemap.xml$', cache_page(sitemap_views.sitemap, 60 * 60 * 6), {'sitemaps': sitemaps}),
        (r'^robots.txt$', 'pulog.views.utils.robots_txt'),
        (r'^favicon.ico$', 'pulog.views.utils.favicon_view'),
        (r'^admin/(.*)', admin.site.root),
        (r'^static/(?P<path>.*)$', 'pulog.media_serve.serve', 
            {'document_root': settings.MEDIA_ROOT}),
        (r'^media/(?P<path>.*)$', 'pulog.media_serve.serve', 
            {'document_root': settings.ADMIN_MEDIA_ROOT}),
        (r'^feed/$', 'pulog.views.utils.redirect_feed'),
        (r'^rss/$', 'pulog.views.utils.redirect_feed'),
        url(r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', 
            {'feed_dict': feed}, name = 'feed'),
)

urlpatterns += patterns('pulog.views.utils',
    (r'^upload/$', 'upload'),
)

urlpatterns += patterns('pulog.views.favourites',
    (r'^favourites/$', 'index'),
    url(r'^favourites/(?P<id>\d+).html$', 'single', name = 'favourite-single'),
)

urlpatterns += patterns('pulog.views',
    (r'^$', 'index'),
    (r'^archives/$', 'index'),
    url(r'^archives/(?P<post_id>\d+).html$', 'single_post', name = 'post-single'),
    url(r'^archives/category/(?P<slug>[-\w]+)/$', 'category_view', name = 'post-category'),
    (r'^archives/category/(?P<slug>[-\w]+)/page/(?P<page_num>\d+)/$', 
        'category_view'),
    url(r'^archives/tag/(?P<slug>[-\w]+)/$', 'tag_view', name = 'post-tag'),
    (r'^archives/tag/(?P<slug>[-\w]+)/page/(?P<page_num>\d+)/$', 
        'tag_view'),
    (r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive_view'),
    (r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page_num>\d+)/$',
        'archive_view'),
    (r'^page/(?P<num>\d+)/$', 'page'),
    (r'^([-\w]+)/$', 'static_pages'),
#   (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page_num>\d+)$', 'archive_view'),
)

urlpatterns += patterns('pulog.views',
    url(r'^comment/post/$',          'comment.post_comment',       name='comment-post-comment'),
    url(r'^comment/posted/$',        'comment.comment_done',       name='comment-comment-done'),
    url(r'^comment/flag/(\d+)/$',    'moderation.flag',             name='comment-flag'),
    url(r'^comment/flagged/$',       'moderation.flag_done',        name='comment-flag-done'),
    url(r'^comment/delete/(\d+)/$',  'moderation.delete',           name='comment-delete'),
    url(r'^comment/deleted/$',       'moderation.delete_done',      name='comment-delete-done'),
    url(r'^comment/moderate/$',      'moderation.moderation_queue', name='comment-moderation-queue'),
    url(r'^comment/approve/(\d+)/$', 'moderation.approve',          name='comment-approve'),
    url(r'^comment/approved/$',      'moderation.approve_done',     name='comment-approve-done'),
)
