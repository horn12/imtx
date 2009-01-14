from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from pulog.models import Category
from pulog.models import Post
from pulog.models import Link
from pulog.models import Profile
from pulog.models import Media
from pulog.models import Comment
from pulog.models import Tag
from pulog.models import TaggedItem
from pulog.models import Favourite

#TODO In tiny_mce, implement the StackedInline
class MediaAdmin(admin.StackedInline):
    model = Media

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author', 'status')
    list_filter = ('date', 'author', 'category', 'type', 'status')
    prepopulated_fields = {'slug': ('title',)}
    radio_fields = {
        'status': admin.VERTICAL,
        'type': admin.VERTICAL
    }
    search_fields = ('title', 'author', 'content')

    class Media:
        js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/textareas.js',
        )

class CommentsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk', 'site')}
        ),
        (_('Content'),
           {'fields': ('user', 'user_name', 'user_email', 'user_url', 'content')}
        ),
        (_('Metadata'),
           {'fields': ('date', 'ip_address', 'is_public', 'is_removed', 'parent', 'mail_notify')}
        ),
     )

    list_display = ('name', 'content_type', 'object_pk', 'ip_address', 'date', 'is_public', 'is_removed')
    list_filter = ('date', 'is_public', 'is_removed')
    date_hierarchy = 'date'
    ordering = ('-date',)
    search_fields = ('content', 'user__username', 'user_name', 'user_email', 'user_url', 'ip_address')

class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'tag')

    class Media:
        js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/textareas.js',
        )

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Link)
admin.site.register(Media)
admin.site.register(Tag)
admin.site.register(TaggedItem)
admin.site.register(Favourite, FavouriteAdmin)
