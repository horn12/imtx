from django.conf.urls.defaults import *

urlpatterns = patterns('imtx_cn.tagging.views',
    url(r'^(?P<slug>[-\w]+)/$', 'tag_view', name = 'tag-view'),
)
