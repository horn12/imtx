from django.contrib import admin
from pulog.models import Category
from pulog.models import Post
from pulog.models import Link
from pulog.models import Profile
from pulog.models import Media

class MediaAdmin(admin.StackedInline):
    model = Media

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author')
    prepopulated_fields = {'slug': ('title',)}
    radio_fields = {
        'status': admin.VERTICAL,
        'type': admin.VERTICAL
    }
    inlines = [MediaAdmin,]

    class Media:
        js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/textareas.js',
        )

admin.site.register(Media)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Link)
