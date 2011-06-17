from __future__ import with_statement
import os
import sys
import glob
from fabric.api import *
from fabric.contrib.console import confirm

env.user = os.getenv('IMTX_USER')
env.hosts = [os.getenv('IMTX_HOST')]

def get_mysql_password():
    sys.path.insert(0, os.getcwd())
    import imtx.settings
    return imtx.settings.DATABASES['default']['PASSWORD']

def createdb():
    local('mysql -uroot -p%s -e "create database imtx_me"' % get_mysql_password())

def dropdb():
    local('mysql -uroot -p%s -e "drop database imtx_me"' % get_mysql_password())

def sync():
    if get_mysql_password():
        try:
            dropdb()
        except:
            pass
        createdb()
    tar_list = glob.glob(os.path.expanduser('~/Dropbox/imtx-backup/*.tar.gz'))
    tar_list.sort()
    tar = tar_list[-1]

    local('cd .. && tar zxf %s imtx/imtx/static/' % tar, capture=False)
    local('cd .. && tar zxf %s imtx/imtx/local_settings.py' % tar, capture=False)
    if os.uname()[0] == 'Darwin':
        local("gsed -i 's/DEBUG = False/DEBUG = True/g' imtx/local_settings.py", capture=False)
    else:
        local("sed -i 's/DEBUG = False/DEBUG = True/g' imtx/local_settings.py", capture=False)

    mysql_password = get_mysql_password()
    sql_list = glob.glob(os.path.expanduser('~/Dropbox/imtx-backup/*.sql.gz'))
    sql_list.sort()
    sql = sql_list[-1]
    base_name = os.path.basename(sql)
    local('rm -rf /tmp/imtx*')
    local('cp %s /tmp/%s' % (sql, base_name))
    local('gunzip /tmp/%s' % base_name)
    local('mysql -uroot -p%s imtx_me < /tmp/%s' % (mysql_password, base_name[:-3]))
    local('rm /tmp/%s' % base_name[:-3])

def install():
    local('pip install -r stable-requirements.txt', capture=False)

def runserver():
    local('cd imtx && python manage.py runserver', capture=False)

def deploy(run_pip='no'):
    with cd('~/public_html/imtx.me/imtx'):
        run('git pull origin master')
        if run_pip != 'no':
            run('/home/tualatrix/public_html/imtx.me/bin/pip install -r stable-requirements.txt')
        run('touch django.wsgi')

def migrate():
    with cd('~/public_html/imtx.me/imtx/imtx'):
        run('/home/tualatrix/public_html/imtx.me/bin/python manage.py migrate')
        run('touch django.wsgi')

def shell():
    with cd('imtx'):
        local('python manage.py shell', capture=False)
