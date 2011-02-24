from __future__ import with_statement
import os
from fabric.api import *
from fabric.contrib.console import confirm

env.user = os.getenv('IMTX_USER')
env.hosts = [os.getenv('IMTX_HOST')]

def deploy():
    with cd('www/imtx.cn/imtx.cn/'):
        run('git pull origin master')
        run('touch ~/www/imtx.cn/cgi-bin/imtxcn.fcgi')
