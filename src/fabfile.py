#! -*- coding: utf-8 -*-

from fabric.api import env
from fabric.context_managers import cd, prefix
from fabric.contrib import files
import os
from random import choice
from fabric.operations import run, get, local

env.hosts = ['xxx',]
env.user = "xxx"
env.sitename = 'xxx'

env.repo = 'xxx'

env.db_user = "xxx"
env.db_name = "xxx"
env.db_password = "xxx"

env.email_user = env.email_from = "noreply@%s" % env.sitename
env.email_password = ""
env.secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

env.local_project_dir = os.path.realpath(os.path.join(os.path.dirname(env.real_fabfile), ))
env.remote_project_dir = '/home/%s/web/%s/private' % (env.user, env.sitename,)
env.remote_web_dir = '/home/%s/web/%s/public_html' % (env.user, env.sitename,)


def install_new_project():
    # WARNING: CREATE A FULLY NEW PROJECT
    with cd(env.remote_project_dir):

        run('mkdir -p logs')
        run('touch logs/project.log')

        run('git clone %s project' % env.repo)
        run('virtualenv --no-site-packages env')

        with prefix('source env/bin/activate'):
            run('pip install -r project/requirements.txt')

        with cd('project/src'):
            with prefix('source ../../env/bin/activate'):

                files.upload_template("%s/../deploy/settings_local.py" % env.local_project_dir,
                    "%s/project/src/main/settings_local.py" % (env.remote_project_dir, ), context=env, backup=False
                )

                run('python manage.py syncdb --noinput')
                run('python manage.py migrate')
                run('python manage.py collectstatic --noinput')

    with cd(env.remote_web_dir):
        run('ln -sf %s/project/src/static/  static' % (env.remote_project_dir, ))
        run('ln -sf %s/project/src/media/  media' % (env.remote_project_dir, ))

        files.upload_template("%s/../deploy/.htaccess" % env.local_project_dir,
            "%s/.htaccess" % env.remote_web_dir, context=env, backup=False
        )
        files.upload_template("%s/../deploy/django.wsgi" % env.local_project_dir,
            "%s/django.wsgi" % env.remote_web_dir, context=env, backup=False
        )
        files.upload_template("%s/../deploy/robots.txt" % env.local_project_dir,
            "%s/robots.txt" % env.remote_web_dir, context=env, backup=False
        )

    with cd(env.remote_project_dir):
        run('ln -sf %s/django.wsgi  %s/project/src/django.wsgi' % (env.remote_web_dir, env.remote_project_dir ))


def up():
    with cd(env.remote_project_dir):
        with prefix('source %s/env/bin/activate' % env.remote_project_dir):
            with cd('project/src/'):
                run('git pull')
                run('python manage.py syncdb --noinput')
                run('python manage.py migrate')
                run('python manage.py collectstatic --noinput')
                run('touch django.wsgi')


def grab_copy():
    with cd(env.remote_project_dir):
        with cd('project/src/'):
            run('tar cjf media.tar.bz2 media')
            run('mysqldump -uxxx xxx -pxxx > dump.sql')
            get('media.tar.bz2', env.local_project_dir)
            get('dump.sql',  env.local_project_dir)
            local('rm -rf media')
            local('tar xjf media.tar.bz2')
            local('mysqladmin -uxxx -pxxx drop moskrc_kot -f')
            local('mysqladmin create -uxxx -pxx moskrc_kot')
            local('mysql moskrc_kot -uxxx -pxxx < dump.sql')
            local('rm media.tar.bz2')
            local('rm dump.sql')

