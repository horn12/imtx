from django.contrib.syndication.feeds import Feed  
from pulog.models import Post
from pulog.models import Comment

class LatestPosts(Feed):
	title = "I'm TualatriX"
	link = '/'
	description = "Hello! This is TualatriX's blog"
	author = 'TualatriX'
	title_template = 'feed/latest_title.html'
	description_template = 'feed/latest_description.html'

	def items(self):
		posts = Post.objects.get_post()[:10]
		return posts

class LatestCommentFeed(Feed):
    """Feed of latest comments on the current site."""

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return u"%s comments" % self._site.name

    def link(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "http://%s/" % (self._site.domain)

    def description(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return u"Latest comments on %s" % self._site.name

    def items(self):
        qs = Comment.objects.filter(
            site__pk = settings.SITE_ID,
            is_public = True,
            is_removed = False,
        )
        if getattr(settings, 'COMMENTS_BANNED_USERS_GROUP', None):
            where = ['user_id NOT IN (SELECT user_id FROM auth_user_groups WHERE group_id = %s)']
            params = [settings.COMMENTS_BANNED_USERS_GROUP]
            qs = qs.extra(where=where, params=params)
        return qs.order_by('-date')[:40]
        
    def item_pubdate(self, item):
        return item.date
