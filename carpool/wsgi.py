# -*- coding: utf-8 -*-

"""WSGI config for the CarPool web application.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carpool.settings")
django.setup()
