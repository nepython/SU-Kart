"""
WSGI config for SU_Kart project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
#Changes are made here as Static files were not getting imported
import os
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SU_Kart.settings')
if settings.DEBUG:
    application = StaticFilesHandler(get_wsgi_application())
else:
    application =get_wsgi_application()