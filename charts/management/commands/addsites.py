from django.core.management.base import BaseCommand
from charts.site_data import populate


class Command(BaseCommand):
    help = 'Dump data'

    def handle(self, *args, **options):
        populate()