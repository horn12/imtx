import os
from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page

from imtx_cn.blog.models import Post, Page, Category, Favourite
from imtx_cn.blog.feeds import LatestPosts

admin.autodiscover()

class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Page.objects.get_page()

    def lastmod(self, obj):
        return obj.date

class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.2

    def items(self):
        return Post.objects.get_post()

    def lastmod(self, obj):
        return obj.date

class FavSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.2

    def items(self):
        return Favourite.objects.all()

    def lastmod(self, obj):
        return obj.pub_date

sitemaps = {
    'posts': PostSitemap,
    'pages': PageSitemap,
    'favourites': FavSitemap,
}

feed = {
    'latest': LatestPosts,
}

urlpatterns = patterns('',
#        (r'linebreak/', 'imtx_cn.blog.views.break_lines'),
        (r'^sitemap.xml$', cache_page(sitemap_views.sitemap, 60 * 60 * 6), {'sitemaps': sitemaps}),
        (r'^search/', 'imtx_cn.blog.views.search'),
        (r'^admin/(.*)', admin.site.root),
        (r'^static/(?P<path>.*)$', 'imtx_cn.media_serve.serve', 
            {'document_root': settings.MEDIA_ROOT}),
        (r'^media/(?P<path>.*)$', 'imtx_cn.media_serve.serve', 
            {'document_root': settings.ADMIN_MEDIA_ROOT}),
        (r'^feed/$', 'imtx_cn.blog.views.redirect_feed'),
        (r'^rss/$', 'imtx_cn.blog.views.redirect_feed'),
        url(r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', 
            {'feed_dict': feed}, name = 'feed'),
        (r'^comment/', include('imtx_cn.comments.urls')),
        (r'^tag/', include('imtx_cn.tagging.urls')),
        (r'^comments/$', 'imtx_cn.comments.views.comment_list'),
)

urlpatterns += patterns('imtx_cn.blog.views',
    (r'^upload/$', 'upload'),
)

urlpatterns += patterns('imtx_cn.blog.views',
    (r'^favourites/$', 'index'),
    url(r'^favourites/(?P<id>\d+).html$', 'single_favourite', name = 'favourite-single'),
)

urlpatterns += patterns('imtx_cn.blog.views',
    (r'^$', 'index'),
    (r'^index.html$', 'index'),
    (r'^archives/$', 'index'),
    url(r'^archives/(?P<post_id>\d+).html$', 'single_post', name = 'post-single'),
    url(r'^archives/category/(?P<slug>[-\w]+)/$', 'category_view', name = 'post-category'),
    (r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive_view'),
    (r'^([-\w]+)/$', 'static_pages'),
)
