from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Category, Post, Link, Profile, Media

#TODO In tiny_mce, implement the StackedInline
class MediaAdmin(admin.StackedInline):
    model = Media

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author', 'status')
    list_filter = ('date', 'author', 'category', 'type', 'status')
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

class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'tag')

    class Media:
        js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/textareas.js',
        )

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Link)
admin.site.register(Media)
