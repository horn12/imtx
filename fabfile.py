from __future__ import with_statement
import os
from fabric.api import *
from fabric.contrib.console import confirm

env.user = os.getenv('IMTX_USER')
env.hosts = [os.getenv('IMTX_HOST')]

def deploy():
    with cd('~/public_html/imtx.me/imtx'):
        run('git pull origin master')
        run('touch django.wsgi')
