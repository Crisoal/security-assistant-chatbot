import os

from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'django' command-line utility
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'security_assistant.settings')

# Get the WSGI application
application = get_wsgi_application()
