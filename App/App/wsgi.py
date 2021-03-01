"""
WSGI config for App project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'App.settings')

application = get_wsgi_application()

# TODO add note about this in report
# call_command("flush", "--noinput")
# call_command("makemigrations", "--noinput")
# call_command("migrate", "--noinput")
