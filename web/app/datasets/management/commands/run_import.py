from django.core.management.base import BaseCommand, CommandError

from datasets.imports import load_data


class Command(BaseCommand):
    help = 'Import datasets relevant for Energie transitie project'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir', dest='dir', type=str,
            help='Directory to load datafiles from (default /data).')

    def handle(self, *args, **options):
        self.stdout.write('First stage of import process beginning:')
        self.stdout.write('(Assumes data files have been downloaded!')
        target_dir = options['dir'] if options['dir'] is not None else '/data'
        load_data.main(target_dir)

        self.stdout.write('Done')
