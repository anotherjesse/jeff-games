import os, sys
sys.path.append('/var/www/projects')
os.environ['DJANGO_SETTINGS_MODULE'] = 'jeffgame.settings'

import django.core.handlers.wsgi
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
