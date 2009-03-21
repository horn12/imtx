from django.conf.urls.defaults import *

urlpatterns = patterns('imtx.apps.tagging.views',
    url(r'^(?P<slug>[-\w]+)/$', 'tag_view', name = 'tag-view'),
)
