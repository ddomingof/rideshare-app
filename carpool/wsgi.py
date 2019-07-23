# -*- coding: utf-8 -*-

import os
from django.core.wsgi import get_wsgi_application
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carpool.settings")
django.setup()

application = get_wsgi_application()
