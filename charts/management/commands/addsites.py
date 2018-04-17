from django.core.management.base import BaseCommand
from charts.models.site import Site


class Command(BaseCommand):
    help = 'Dump data'

    def handle(self, *args, **options):
        Site.populate()