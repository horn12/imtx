import time
import datetime

from django.db.models import Q
from django.contrib.syndication.feeds import Feed  

from models import Post
from imtx.apps.comments.models import Comment

class LatestPosts(Feed):
    title = "I'm TualatriX"
    link = 'http://imtx.me/'
    description = "Hello! This is TualatriX's blog"
    author = 'TualatriX'
    title_template = 'feed/latest_title.html'
    description_template = 'feed/latest_description.html'

    def items(self):
        #TODO What's the meaning of lte?
        return Post.objects.get_post().filter(date__lte=datetime.datetime.now())[:10]

    def item_pubdate(self, item):
        return item.date

class LatestCommentFeed(Feed):
    """Feed of latest comments on the current site."""
    title = "I'm TualatriX"
    link = 'http://imtx.me/'
    description = "Hello! This is TualatriX's blog's comments"
    title_template = 'feed/latest_comment_title.html'
    description_template = 'feed/latest_comment_description.html'

    def items(self):
        return Comment.objects.in_public().filter(~Q(user_email="tualatrix@gmail.com"))[:10]
        
    def item_pubdate(self, item):
        return item.date
