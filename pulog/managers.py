from django.db import models
from django.dispatch import dispatcher
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

class CommentManager(models.Manager):

    def in_moderation(self):
        """
        QuerySet for all comments currently in the moderation queue.
        """
        return self.get_query_set().filter(is_public=False, is_removed=False)

    def for_model(self, model):
        """
        QuerySet for all comments for a particular model (either an instance or
        a class).
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_query_set().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_unicode(model._get_pk_val()))
        return qs

class PostManager(models.Manager):
    def get_post(self):
        return self.get_query_set().filter(
                    type = self.model.POST_TYPE,
                    status = self.model.PUBLISHED_STATUS).order_by('-date')
    
    def get_page(self):
        return self.get_query_set().filter(
                    type = self.model.PAGE_TYPE,
                    status = self.model.PUBLISHED_STATUS)
        
    def get_post_by_category(self, cat):
        return self.get_query_set().filter(
                type = self.model.POST_TYPE,
                status = self.model.PUBLISHED_STATUS,
                category = cat.id).order_by('-date')
        
    def get_post_by_date(self, year, month):
        return self.get_query_set().filter(
                type = self.model.POST_TYPE,
                status = self.model.PUBLISHED_STATUS,
                date__year = int(year),
                date__month = int(month)).order_by('-date')
