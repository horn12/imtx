from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from pulog.models import Category
from pulog.models import Post
from pulog.models import Link
from pulog.models import Profile
from pulog.models import Media
from pulog.models import Comment

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
#    inlines = [MediaAdmin,]
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
           {'fields': ('user', 'user_name', 'user_email', 'user_url', 'comment')}
        ),
        (_('Metadata'),
           {'fields': ('date', 'ip_address', 'is_public', 'is_removed')}
        ),
     )

    list_display = ('name', 'content_type', 'object_pk', 'ip_address', 'date', 'is_public', 'is_removed')
    list_filter = ('date', 'site', 'is_public', 'is_removed')
    date_hierarchy = 'date'
    ordering = ('-date',)
    search_fields = ('comment', 'user__username', 'user_name', 'user_email', 'user_url', 'ip_address')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Link)
admin.site.register(Media)
