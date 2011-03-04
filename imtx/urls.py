import os
from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page

from imtx.apps.blog.models import Post, Category
from imtx.apps.blog.feeds import LatestPosts, LatestCommentFeed

admin.autodiscover()

class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.2

    def items(self):
        return Post.objects.get_post()

    def lastmod(self, obj):
        return obj.date

sitemaps = {
    'posts': PostSitemap,
}

feed = {
    'latest': LatestPosts,
    'comments': LatestCommentFeed,
}

urlpatterns = patterns('',
    (r'^sitemap.xml$', cache_page(sitemap_views.sitemap, 60 * 60 * 6), {'sitemaps': sitemaps}),
    (r'^admin/', include(admin.site.urls)),
    url(r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', 
        {'feed_dict': feed}, name='feed'),
    (r'^comment/', include('imtx.apps.comments.urls')),
    (r'^tag/', include('imtx.apps.tagging.urls')),
    (r'^comments/$', 'imtx.apps.comments.views.comment_list'),
    (r'^xmlrpc/$', 'django_xmlrpc.views.handle_xmlrpc', {}, 'xmlrpc'),
)

urlpatterns += patterns('imtx.apps.blog.views',
    (r'^upload/$', 'upload'),
    (r'^search/', 'search'),
    (r'^feed/$', 'redirect_feed'),
    (r'^rss/$', 'redirect_feed'),
    (r'^$', 'index'),
    (r'^index.html$', 'index'),
    (r'^archives/$', 'index'),
    url(r'^archives/(?P<post_id>\d+).html$', 'single_post', name='single_post'),
    url(r'^archives/category/(?P<slug>[-\w]+)/$', 'category_view', name='post-category'),
    (r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive_view'),
    url(r'^([-\w]+)/$', 'static_pages', name='static_pages'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
