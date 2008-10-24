from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import encoding, html
from django.utils.html import urlquote

class Category(models.Model):
    title = models.CharField(max_length = 250, help_text = 'Maximum 250 \
            characters.')
    slug = models.SlugField(unique = True, help_text = 'Suggested value \
            automatically generated from title. Must be unique.')
    description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.title

    def get_post_count(self):
        return len(Post.objects.filter(type = 'post', category = self.id))

    def get_absolute_url(self):
        return '/archives/category/%s' % self.slug

class Tag(models.Model):
    '''Tag entity'''
    name = models.CharField('Name', unique = True, max_length = 64)
    slug = models.CharField('Slug', max_length = 255, unique = True,\
            blank = True, help_text = 'Use as url')
    reference_count = models.IntegerField('Reference count', default = 0,\
            editable = False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/tag/%s/' % self.slug

class Profile(models.Model):
	user = models.ForeignKey(User, unique = True)

	nickname = models.CharField(max_length = 30)
	website = models.URLField(blank = True)

	def save(self):
		if not self.nickname:
			self.nickname = self.user.username
		super(Profile, self).save()

	def __unicode__(self):
		return self.nickname

	class Admin:
		pass

class Post(models.Model):
    TYPE_CHOICES = (
            ('page', 'Page'),
            ('post', 'Post'),
            )
    POST_STATUS_CHOICES = (
            ('publish', 'Published'),
            ('pending', 'Pending Review'),
            ('draft', 'Unpublished'),
            )
    COMMENT_STATUS_CHOICES = (
            ('open', 'Open'),
            ('closed', 'Closed'),
            )
    title = models.CharField(max_length = 64)
    name = models.CharField(max_length = 200, blank = True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User)
    category = models.ManyToManyField(Category)
    view = models.IntegerField(default = 0, editable = False)
    type = models.CharField(max_length = 20, default = 'post', choices = TYPE_CHOICES)
    post_status = models.CharField(max_length = 20, default = 'publish', choices = POST_STATUS_CHOICES)
    comment_status = models.CharField(max_length = 20, default = 'open', choices = COMMENT_STATUS_CHOICES)
    tags = models.ManyToManyField(Tag, blank = True, related_name = 'post_set')

    def save(self):
        self.content = html.clean_html(self.content)
        super(Post, self).save()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/archives/%d.html' % self.id

    def get_author(self):
        try:
            profile = self.author.get_profile()
        except Exception:
            name = self.author.username
        else:
            name = profile.nickname

        return name

    def get_views_count(self):
        return self.view

    def get_comments(self):
        comments = self.comments.order_by('id')
        return comments

    def get_comments_count(self):
        comments = self.comments.order_by('id')
        return len(comments)

    def get_excerpt(self):
        return self.content.split('<!--more-->')[0]

    def get_remain(self):
        return self.content.split('<!--more-->')[1]

    def get_pagebreak(self):
        try:
            self.content.index('<!--more-->')
        except ValueError:
            return ''
        else:
            return 'true'

    def get_categories(self):
        return self.category.all()

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name = 'comments')
    author = models.CharField(max_length = 32)
    email = models.EmailField()
    url = models.URLField(blank = True)
    IP = models.IPAddressField(editable = False)
    date = models.DateTimeField(auto_now_add = True, editable = False)
    content = models.TextField()

    def __unicode__(self):
        return '%s: %s' % (self.author, self.content)

    def get_display(self):
        return html.strip_tags(self.content)

    def get_absolute_url(self):
        return '%s#comment-%d' % (self.post.get_absolute_url(), self.id )

class Link(models.Model):
    url = models.URLField()
    name = models.CharField(max_length = 255)
    description = models.TextField()

    def __unicode__(self):
        return '%s: %s' % (self.name, self.url)
