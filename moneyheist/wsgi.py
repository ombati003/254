"""
WSGI config for moneyheist project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import os
#from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneyheist.settings')

application = get_wsgi_application()




"""class CustomSentry(MiddlewareMixin,):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception): 
        return HttpResponse("in exception")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = CustomSentry(get_wsgi_application())"""
