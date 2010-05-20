from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

def deploy():
    with cd('www/imtx.cn/imtx.cn/'):
        run('git pull origin master')
        run('touch ~/www/imtx.cn/cgi-bin/imtxcn.fcgi')
