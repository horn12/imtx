from django.contrib import admin
from pulog.models import Category
from pulog.models import Post
from pulog.models import Link
from pulog.models import Profile

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author')
    radio_fields = {'post_status': admin.VERTICAL,
                    'type': admin.VERTICAL,
                    'comment_status': admin.VERTICAL}

    class Media:
        js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/textareas.js',
        )

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Link)
