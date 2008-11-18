from django.db import models
from django.dispatch import dispatcher
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

class CommentManager(models.Manager):

    def in_public(self):
        return self.get_query_set().filter(is_public = True, is_removed = False).order_by('date')

    def in_moderation(self):
        """
        QuerySet for all comments currently in the moderation queue.
        """
        return self.get_query_set().filter(is_public=False, is_removed=False)

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
        def append_comment_start(comment, html):
            html.append('<li class="comment even thread-even depth-%(depth)d" id="comment-%(id)d">\n'
                '<div id="div-comment-%(id)d"><div class="comment-author vcard"><cite><a href="http://wordpress.org/" rel="external nofollow">%(name)s</a></cite> Says: </div>\n'
               '<div class="comment-meta commentmetadata"><a href="%(url)s">November 12th, 2008 at 2:24 pm</a>&nbsp;&nbsp;<a href="http://127.0.0.1/wordpress/wp-admin/comment.php?action=editcomment&amp;c=1" title="Edit comment">edit</a></div>\n'
               '<p>%(content)s</p>\n'
               '<div class="reply"><a rel="nofollow" href="/wordpress/archives/1/comment-page-1?replytocom=1#respond" onclick=\'return addComment.moveForm("div-comment-1", "1", "respond")\'>Reply</a></div></div>\n\n'
                % {
                    'depth': comment.get_depth(),
                    'id': comment.id,
                    'url': comment.url,
                    'name': comment.name,
                    'content': comment.content,
                })
        def append_comment_end(html):
            html.append('</li>\n')

        def append_child_start(html):
            html.append('<ul class="children">\n')

        def append_child_end(html):
            html.append('</ul>\n')

        def create_comment_html(root, list, html):
            append_comment_start(root, html)
            print root.content
            list.remove(root)
            if root.has_children():
                children = root.get_children()
                print 'the children of %s: %s' % (root, children)
                for child in children:
                    print 'child', child.content
                    append_child_start(html)
                    create_comment_html(child, list, html)
#                    append_child_end(html)
                    print 'end of child', child.content

            append_comment_end(html)
            if root.has_parent():
                append_child_end(html)

            print 'end of root', root.content

#            if root.has_parent() and not root.has_children():
#                append_comment_end(html)
#                append_child_end(html)

            #FIXME
            if len(list) > 0 and not root.has_parent():
                create_comment_html(list[0], list, html)

        def sort_comment(root, list, sorted, html):
            if root.has_parent():
                append_child_start(html)
            append_comment_start(root, html)
            sorted.append(root)
            list.remove(root)
            if root.has_children():
                children = root.get_children()
                for child in children:
#                    append_child_start(html)
                    sort_comment(child, list, sorted, html)
#                    append_child_end(html)
                append_comment_end(html)
            else:
                append_comment_end(html)
                append_child_end(html)

            if len(list) > 0:
                sort_comment(list[0], list, sorted, html)

        comments = list(qs)

        html = []
        if comments:
            comments = list(qs)
            sorted = []
            first = comments[0]
            html.append('<ol class="commentlist">\n')
#            sort_comment(first, comments, sorted, html)
            create_comment_html(first, comments, html)
            print sorted
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
