from django.core.management.base import BaseCommand

from bulbs.utils.percolator import clean_deprecated_class_percolators, get_deprecated_queries


class Command(BaseCommand):
    help = 'clean out deprecated or bad percolator queries'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check',
            action='store_true',
            dest='check',
            default=False,
            help='Print out list of bad query ids'
        )

    def handle(self, *args, **kwargs):
        if kwargs['check']:
            bad_queries = get_deprecated_queries()
            self.stdout.write('\n'.join(bad_queries))
        else:
            clean_deprecated_class_percolators()
