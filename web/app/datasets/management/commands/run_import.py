from django.core.management.base import BaseCommand, CommandError

from datasets.imports import load_data
from datasets.imports import handelsregister
from datasets.imports import bag_brk_api


class Command(BaseCommand):
    help = 'Import datasets relevant for Energie transitie project'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir', dest='dir', type=str,
            help='Directory to load datafiles from (default /data).')

        parser.add_argument(
            '--handelsregister', default=False, action='store_true',
            help='Load handelsregister data for all neighborhoods')

        parser.add_argument(
            '--sbicodes', default=False, action='store_true',
            help='Load sbi data')

        parser.add_argument(
            '--hrrapport', default=False, action='store_true',
            help='Fill hr summary information viewset')

        parser.add_argument(
            '--brkbag', default=False, action='store_true',
            help='Load brk bag')

    def handle(self, *args, **options):

        if options['handelsregister']:
            handelsregister.get_hr_for_all_buurten()
            return

        if options['sbicodes']:
            handelsregister.get_sbi_code_meta()
            return

        if options['hrrapport']:
            handelsregister.create_tabledata_hr_per_buurt()
            return

        if options['brkbag']:
            bag_brk_api.get_bag_brk_for_all_buurten()
            return

        self.stdout.write('First stage of import process beginning:')
        self.stdout.write('(Assumes data files have been downloaded!')

        target_dir = options['dir'] if options['dir'] is not None else '/data'
        load_data.main(target_dir)

        self.stdout.write('Done')
