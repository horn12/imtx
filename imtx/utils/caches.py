#
# cache interface
#
from django.core.cache import cache
from imtx.settings import *

def _format_key(key):
	"""add prefix to key"""
	return '%s/%s' % (CACHE_PREFIX,key)

def set(key,value):
	return cache.set(_format_key(key),value)
	
def get(key):
	return cache.get(_format_key(key))
	
def delete(key):
	cache.delete(_format_key(key))
	
def get_many(keys = []):
	cache.get_many(keys.e)