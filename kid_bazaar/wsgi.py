"""
WSGI config for kid_bazaar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kid_bazaar.settings")

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()


## HEROKU WSGI ##

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
