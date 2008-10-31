from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import encoding, html
from django.utils.html import urlquote
from django.db.models.fields.files import ImageFieldFile

import tagging

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
        return len(Post.manager.get_post_by_category(self))

    def get_absolute_url(self):
        return '/archives/category/%s/' % self.slug

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

class PostManager(models.Manager):
    def get_post(self):
        return self.get_query_set().filter(type = self.model.POST_TYPE).order_by('-date')

    def get_page(self):
        return self.get_query_set().filter(type = self.model.PAGE_TYPE).order_by('-date')

    def get_post_by_category(self, cat):
        return self.get_query_set().filter(type = self.model.POST_TYPE, 
                category = cat.id).order_by('-date')

    def get_post_by_date(self, year, month):
        return self.get_query_set().filter(type = self.model.POST_TYPE, 
                date__year = int(year),
                date__month = int(month)).order_by('-date')

class Post(models.Model):
    (
        PAGE_TYPE,
        POST_TYPE,
    ) = range(2)
    (
        PUBLISHED_STATUS,
        PENDING_STATUS,
        DRAFT_STATUS,
    ) = range(3)

    TYPE_CHOICES = (
        (PAGE_TYPE, _('Page')),
        (POST_TYPE, _('Post')),
    )
    STATUS_CHOICES = (
        (PUBLISHED_STATUS, _('Published')),
        (PENDING_STATUS, _('Pending Review')),
        (DRAFT_STATUS, _('Unpublished')),
    )
    title = models.CharField(max_length = 64)
    slug = models.SlugField(unique = True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User)
    category = models.ManyToManyField(Category)
    view = models.IntegerField(default = 0, editable = False)
    type = models.IntegerField(default = POST_TYPE, choices = TYPE_CHOICES)
    status = models.IntegerField(default = PUBLISHED_STATUS, choices = STATUS_CHOICES)
    enable_comment = models.BooleanField(default = True)
    manager = PostManager()
    objects = models.Manager()

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

    def __get_excerpt(self):
        return self.content.split('<!--more-->')[0]

    excerpt = property(__get_excerpt)

    def __get_remain(self):
        return self.content.split('<!--more-->')[1]

    remain = property(__get_remain)

    def __get_pagebreak(self):
        try:
            self.content.index('<!--more-->')
        except ValueError:
            return False
        else:
            return True
    pagebreak = property(__get_pagebreak)

    def get_categories(self):
        return self.category.all()

tagging.register(Post)

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

class Media(models.Model):
    UPLOAD_ROOT = 'upload/%Y/%m'

    title = models.CharField(max_length = 120)
    image = models.ImageField(upload_to = UPLOAD_ROOT)
    date = models.DateTimeField(auto_now_add = True)
    post = models.ForeignKey(Post)

    class Meta:
        verbose_name_plural = _('Media')

    def __unicode__(self):
        return _('%s, uploaded at %s') % (self.title, self.date.strftime('%T %h %d, %Y'))
