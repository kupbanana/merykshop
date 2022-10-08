"""
Konfiguracja WSGI dla projektu merykshop.

"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'merykshop.settings')

application = get_wsgi_application()
