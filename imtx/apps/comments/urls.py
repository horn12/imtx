from django.conf.urls.defaults import *

urlpatterns = patterns('imtx.apps.comments.views',
    url(r'^post/$',          'post_comment',       name='comment-post-comment'),
    url(r'^spam/(?P<comment_id>\d+)/$',          'spam_comment',       name='comment-spam-comment'),
)
