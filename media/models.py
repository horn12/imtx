import os
from django.db import models
from settings import MEDIA_ROOT
from django.utils.translation import ugettext as _
from django.db.models.fields.files import ImageFieldFile
from pulog.models import Post

UPLOAD_ROOT = 'upload/%Y/%m'

class Media(models.Model):
    title = models.CharField(max_length = 120)
    image = models.ImageField(upload_to = UPLOAD_ROOT)
    date = models.DateTimeField(auto_now_add = True)
    post = models.ForeignKey(Post)

    class Meta:
        verbose_name_plural = _('Media')

    def __unicode__(self):
        return _('%s, uploaded at %s') % (self.title, self.date.strftime('%T %h %d, %Y'))
