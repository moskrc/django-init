import os, sys
sys.path.insert(0, '/home/%(user)s/web/%(sitename)s/private/env/lib/python2.7/site-packages')
sys.path.insert(0, '/home/%(user)s/web/%(sitename)s/private/project/src')
sys.path.insert(0, '/home/%(user)s/web/%(sitename)s/private/project/src/shared')

os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
