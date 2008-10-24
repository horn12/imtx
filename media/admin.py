from django.contrib import admin
from models import Media

class MediaAdmin(admin.StackedInline):
    model = Media

admin.site.register(Media)
