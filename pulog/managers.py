from django.db import models
from django.dispatch import dispatcher
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.conf import settings

COMMENT_MAX_DEPTH = getattr(settings, 'COMMENT_MAX_DEPTH', 5)

class CommentManager(models.Manager):

    def in_public(self):
        return self.get_query_set().filter(is_public = True, is_removed = False).order_by('-date')

    def in_moderation(self):
        """
        QuerySet for all comments currently in the moderation queue.
        """
        return self.get_query_set().filter(is_public=False, is_removed=False)

    def get_depth_odd(self, depth):
        "Post"
        pass

    def get_sorted_comments(self, qs):
        def sort_comment(root, list, sorted):
            sorted.append(root)
            list.remove(root)
            if root.has_children():
                children = root.get_children()
                for child in children:
                    sort_comment(child, list, sorted)
            elif len(list) > 0 and root.is_last_child():
                sort_comment(list[0], list, sorted)

        comments = list(qs)
        if comments:
            sorted = []
            first = comments[0]
            print comments
            sort_comment(first, comments, sorted)

            return sorted
        else:
            return comments

    def get_comments_list(self, qs):
        comments = list(qs)

        def get_even_or_odd(comment, list):
#            for ct in list:
#                if ct.has_parent():
#                    list.remove(ct)
#            if list.index(comment) % 2 == 1:
            if comment.id % 2 == 1:
                return "even"
            else:
                return "odd"

        def append_comment_start(comment, list, html):
            if not comment.has_parent():
                #TODO author's comment
                html.append('<li class="comment %(parity)s thread-%(parity)s depth-%(depth)d" id="comment-%(id)d">\n' % {
                    'id': comment.id,
                    'depth': comment.get_depth(),
                    'parity': comment.get_parity(),
                })
            else:
                html.append('<li class="comment %(parity)s depth-%(depth)d" id="comment-%(id)d">\n' % {
                    'id': comment.id,
                    'depth': comment.get_depth(),
                    'parity': comment.get_parity(),
                })
            html.append('<div id="div-comment-%(id)d"><div class="comment-author vcard"><cite><a href="%(user_url)s" rel="external nofollow">%(name)s</a></cite> Says: </div>\n'
               '<div class="comment-meta commentmetadata"><a href="%(url)s">%(date)s</a>&nbsp;&nbsp;<a href="%(edit)s" title="Edit comment">edit</a></div>\n'
               '<p>%(content)s</p>\n' 
                % {
                    'id': comment.id,
                    'url': comment.url,
                    'name': comment.user_name,
                    'user_url': comment.user_url,
                    'date': comment.date.strftime('%D %d:%M %Y'),
                    'depth': comment.get_depth(),
                    'edit': comment.get_admin_url(),
                    'content': comment.content,
                    'parity': get_even_or_odd(comment, list),
                })

            if comment.get_depth() < COMMENT_MAX_DEPTH:
                html.append('<div class="reply"><a rel="nofollow" href="%(url)s#respond" onclick=\'return addComment.moveForm("div-comment-%(id)d", "%(id)d", "respond")\'>Reply</a></div></div>\n\n'
                % {
                    'id': comment.id,
                    'url': comment.url,
                })

        def append_comment_end(html):
            html.append('</li>\n')

        def append_child_start(html):
            html.append('<ul class="children">\n')

        def append_child_end(html):
            html.append('</ul>\n')

        def create_comment_html(root, list, html):
            append_comment_start(root, list, html)
            list.remove(root)
            if root.has_children():
                children = root.get_children()
                for child in children:
                    append_child_start(html)
                    create_comment_html(child, list, html)

            append_comment_end(html)
            if root.has_parent():
                append_child_end(html)

            if len(list) > 0 and not root.has_parent():
                create_comment_html(list[0], list, html)

        html = []
        if comments:
            comments = list(qs)
            sorted = []
            first = comments[0]
            html.append('<ol class="commentlist">\n')
            create_comment_html(first, comments, html)
            html.append('</ol>')

        return ''.join(html)

    def get_children_by_id(self, id):
        list = []
        comments = self.get_query_set().filter(is_public = True, is_removed = False).order_by('date')
        for comment in comments:
            if comment.parent_id == id:
                list.append(comment)

        return list

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
        return self.get_query_set().filter(type = 'post', status = 'publish').order_by('-date')
    
    def get_page(self):
        return self.get_query_set().filter(type = 'page', status = 'publish')
        
    def get_post_by_category(self, cat):
        return self.get_query_set().filter(type = 'post', status = 'publish',
                category = cat.id).order_by('-date')
        
    def get_post_by_date(self, year, month):
        return self.get_query_set().filter(type = 'post', status = 'publish',
                date__year = int(year),
                date__month = int(month)).order_by('-date')
