# -*- coding: utf-8 -*-

"""A command to delete expired rows."""

import datetime

from django.core.management.base import BaseCommand

from ui.models import Commute


class Command(BaseCommand):
    """A command to delete expired rows."""

    help = 'Deletes expired rows'

    def handle(self, *args, **options):
        """Handle the command."""
        now = datetime.datetime.now()
        Commute.objects.filter(time__lt=now).delete()
