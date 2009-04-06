from django.db import models
from django.conf import settings
from django.db.models import signals
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.files import ImageFieldFile

from imtx.apps.tagging.models import Tag
from imtx.apps.tagging.fields import TagField
from imtx.apps.comments.models import Comment
from imtx.apps.comments.signals import  comment_save
from managers import PostManager

class Category(models.Model):
    title = models.CharField(max_length = 250, help_text = _('Maximum 250 '
            'characters.'))
    slug = models.SlugField(unique = True, help_text = _('Suggested value '
            'automatically generated from title. Must be unique.'))
    description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.title

    def get_post_count(self):
        '''Return the post number under the category'''
        return Post.objects.get_post_by_category(self).count()

    @models.permalink
    def get_absolute_url(self):
        return ('post-category', [str(self.slug)])

class Post(models.Model):
    TYPE_CHOICES = (
        ('page', _('Page')),
        ('post', _('Post')),
    )
    STATUS_CHOICES = (
        ('publish', _('Published')),
        ('draft', _('Unpublished')),
    )
    title = models.CharField(max_length = 64)
    slug = models.SlugField(blank = True, unique = True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User)
    category = models.ManyToManyField(Category)
    view = models.IntegerField(default = 0, editable = False)
    type = models.CharField(max_length = 20, default = 'post', choices = TYPE_CHOICES)
    status = models.CharField(max_length = 20, default = 'publish', choices = STATUS_CHOICES)
    comments =  generic.GenericRelation(Comment, 
                    object_id_field = 'object_pk',
                    content_type_field = 'content_type')
    comment_count = models.IntegerField(default = 0)
    objects = PostManager()
    tag = TagField()

    def save(self):
        try:
            self.content = html.clean_html(self.content)
        except:
            pass
        super(Post, self).save()

        # Initial the views and comments count to 0 if the PostMeta isn't available
        pm, created = PostMeta.objects.get_or_create(post=self, meta_key='views')
        if created:
            pm.meta_value = '0'
            pm.save()

        pm, created = PostMeta.objects.get_or_create(post=self, meta_key='comments_count')
        if created:
            pm.meta_value = '0'
            pm.save()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        if self.type == 'post':
            return ('single_post', [str(self.id)])
        else:
            return ('static_pages', [str(self.slug)])

    def get_admin_url(self):
        return '/admin/blog/post/%d/' % self.id

    def get_author(self):
        try:
            profile = self.author.get_profile()
        except Exception:
            name = self.author.username
        else:
            name = profile.nickname

        return name

    def get_views_count(self):
        return PostMeta.objects.get(post=self, meta_key='views').meta_value

    def hit_views(self):
        pm = PostMeta.objects.get(post=self, meta_key='views')
        pm.meta_value = str(int(pm.meta_value) + 1)
        pm.save()

    def get_comments_count(self):
        return PostMeta.objects.get(post=self.id, meta_key='comments_count').meta_value

    def hit_comments(self):
        pm = PostMeta.objects.get(post=self, meta_key='comments_count')
        pm.meta_value = str(self.comments.count())
        pm.save()

    def get_comments(self):
        return Comment.objects.for_model(self)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

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

class PostMeta(models.Model):
    post = models.ForeignKey(Post)
    meta_key = models.CharField(max_length=128)
    meta_value = models.TextField()

    def __unicode__(self):
        return '<%s: %s>' % (self.meta_key, self.meta_value)

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

class Link(models.Model):
    url = models.URLField()
    name = models.CharField(max_length = 255)
    description = models.TextField()
    is_public   = models.BooleanField(_('is public'), default = True)

    def __unicode__(self):
        return '%s: %s' % (self.name, self.url)

class Media(models.Model):
    UPLOAD_ROOT = 'uploads/%Y/%m'
    THUMB_SIZE = '640'
    LOGO_SIZE = '48'

    title = models.CharField(max_length = 120)
    image = models.ImageField(upload_to = UPLOAD_ROOT)
    date = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = _('Media')

    def __unicode__(self):
        return _('<Media: %s, uploaded at %s>') % (self.title, self.date.strftime('%I:%M%p, %Y/%m/%d'))

    def get_thumb_url(self):
        return 'http://%s/static/%s' % (Site.objects.get(pk=settings.SITE_ID).domain, self.image.url)
#        return self.image.url + '?width=' + self.THUMB_SIZE

    def get_logo_url(self):
        return self.image.url + '?width=' + self.LOGO_SIZE + '&height=' + self.LOGO_SIZE

from pingback.client import ping_external_links, ping_directories

signals.post_save.connect(
        ping_external_links(content_attr = 'content', url_attr = 'get_absolute_url'),
        sender = Post, weak = False)

#signals.post_save.connect(
#        ping_directories(content_attr = 'content', url_attr = 'get_absolute_url'),
#        sender = Post, weak = False)

def on_comment_save(sender, comment, *args, **kwargs):
    post = comment.object
    post.hit_comments()

comment_save.connect(on_comment_save)
