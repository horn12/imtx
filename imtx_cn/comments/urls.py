from django.conf.urls.defaults import *

urlpatterns = patterns('imtx_cn.comments.views',
    url(r'^post/$',          'post_comment',       name='comment-post-comment'),
)
