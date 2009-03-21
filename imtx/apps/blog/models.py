from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.files import ImageFieldFile

from imtx.apps.tagging.models import Tag
from imtx.apps.tagging.fields import TagField
from imtx.apps.comments.models import Comment
from managers import PostManager, PageManager

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

class Page(models.Model):
    STATUS_CHOICES = (
        ('publish', _('Published')),
        ('draft', _('Unpublished')),
    )
    title = models.CharField(max_length = 64)
    slug = models.SlugField(unique = True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User)
    category = models.ManyToManyField(Category)
    view = models.IntegerField(default = 0, editable = False)
    status = models.CharField(max_length = 20, default = 'publish', choices = STATUS_CHOICES)
    comment =  generic.GenericRelation(Comment, 
                    object_id_field = 'object_pk',
                    content_type_field = 'content_type')
    comment_count = models.IntegerField(default = 0)
    objects = PageManager()
    tag = TagField()

    def save(self):
        try:
            self.content = html.clean_html(self.content)
        except:
            pass
        self.comment_count = self.get_comment_count()
        super(Page, self).save()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('post-single', [str(self.id)])

    def get_admin_url(self):
        return '/admin/pulog/post/%d/' % self.id

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
        return Comment.objects.for_model(self)

    def get_tags(self):
        return list(Tag.objects.get_for_object(self))

    def get_comment_count(self):
        try:
            return Comment.objects.for_model(self).count()
        except:
            return 0

    def get_categories(self):
        return self.category.all()

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
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User)
    category = models.ManyToManyField(Category)
    view = models.IntegerField(default = 0, editable = False)
    type = models.CharField(max_length = 20, default = 'post', choices = TYPE_CHOICES)
    status = models.CharField(max_length = 20, default = 'publish', choices = STATUS_CHOICES)
    comment =  generic.GenericRelation(Comment, 
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
        self.comment_count = self.get_comment_count()
        super(Post, self).save()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('post-single', [str(self.id)])

    def get_admin_url(self):
        return '/admin/pulog/post/%d/' % self.id

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
        return Comment.objects.for_model(self)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def get_comment_count(self):
        try:
            return Comment.objects.for_model(self).count()
        except:
            return 0

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
        return self.image.url
#        return self.image.url + '?width=' + self.THUMB_SIZE

    def get_logo_url(self):
        return self.image.url + '?width=' + self.LOGO_SIZE + '&height=' + self.LOGO_SIZE
