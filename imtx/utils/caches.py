#
# cache interface
#
from django.core.cache import cache
from imtx.settings import *
import logs

# stroe the cache keys for group delete
tag_list = []

def _format_key(key):
    """add prefix to key"""
    return '%s/%s' % (CACHE_PREFIX,key)

def _set(key,value, timeout=None):
    logs.debug('cache set %s' % key)
    return cache.set(_format_key(key),value)
    
def get(key):
    obj = cache.get(_format_key(key))
    if obj:
        logs.debug('cache hit %s' % key)
	return obj
    
def delete(key):
    logs.debug('cache delete %s' % key)
    cache.delete(_format_key(key))
    
def get_many(keys = []):
    cache.get_many(keys.e)
    
def set(key, value, tags=[], timeout=None):
    """
	author: http://stepsandnumbers.com/archive/2009/04/11/setting-and-delete-cache-in-django-with-tags/
    set namespace with cache group
    eg:
        set_with_tags('home/list/p/1',list,['home/list'])
        set_with_tags('home/list/p/2',list,['home/list'])
    """
    for tag in tags:
        tag_list = get(tag)
        if tag_list:
            tag_list.append(key)
        else:
            tag_list = [key]
        _set(tag, tag_list, timeout)
    _set(key, value, timeout)

def delete_by_tags(tags=[]):
    """
	author: http://stepsandnumbers.com/archive/2009/04/11/setting-and-delete-cache-in-django-with-tags/
	delete caches by namespace/tag
	eg:
		delete_by_tags(['home/list'])
		# this will delete home/list/p/1,home/list/p/2 ...
	"""
    for tag in tags:
        tag_list = get(tag)
        if tag_list:
           for key in tag_list:
               delete(key)
        delete(tag)
