import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/tagwiki/tagwiki/ve/lib/python2.5/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/')
sys.path.append('/var/www/tagwiki/')
sys.path.append('/var/www/tagwiki/tagwiki/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'tagwiki.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
