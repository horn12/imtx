from django.contrib.syndication.feeds import Feed  
from pulog.models import Post

class LatestPosts(Feed):
	title = "I'm TualatriX"
	link = '/'
	description = "Hello! This is TualatriX's blog"
	author = 'TualatriX'
	title_template = 'feed/latest_title.html'
	description_template = 'feed/latest_description.html'

	def items(self):
		posts = Post.objects.filter(type = 'post').order_by('-date')
		return posts
