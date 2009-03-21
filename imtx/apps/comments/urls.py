from django.conf.urls.defaults import *

urlpatterns = patterns('imtx.apps.comments.views',
    url(r'^post/$',          'post_comment',       name='comment-post-comment'),
)
