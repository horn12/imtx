from django.conf.urls.defaults import *

urlpatterns = patterns('imtx.blog.views',
    (r'^$', 'index'),
    (r'^index.html$', 'index'),
    (r'^archives/$', 'index'),
    url(r'^archives/(?P<post_id>\d+).html$', 'single_post', name = 'post-single'),
    url(r'^archives/category/(?P<slug>[-\w]+)/$', 'category_view', name = 'post-category'),
    (r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive_view'),
    (r'^([-\w]+)/$', 'static_pages'),
)
