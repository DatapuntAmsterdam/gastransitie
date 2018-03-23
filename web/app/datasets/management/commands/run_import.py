import logging

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from datasets.imports import handelsregister
from datasets.imports import bag_brk_api
from datasets.imports import bag_fix

from datasets.imports.alliander import import_alliander
from datasets.imports.corporatie_bezit import import_corporatie_bezit
from datasets.imports.renovaties import import_renovaties

from datasets.imports.warmtekoude import import_warmtekoude
from datasets.imports.mip import import_mip
from datasets.imports.eigendomskaart import import_eigendomskaart
from datasets.imports.energie_labels import import_energie_labels

# from datasets.imports.cbs import import_cbs


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import datasets relevant for Energie transitie project'

    # object store statische bronnen
    bronnen = {
        'renovaties': import_renovaties,
        'mip': import_mip,  # meerjarig investerings plan
        'corporatie_bezit': import_corporatie_bezit,
        'energielabels': import_energie_labels,
        'alliander': import_alliander,
        # 'eigendomskaart': import_eigendomskaart,
        'warmtekoude': import_warmtekoude
        # 'cbs': import_cbs
    }

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

        parser.add_argument(
            '--indexgebied', default=False, action='store_true',
            help='Index bag gebied 4326')

        # for every bron add flag.
        for key in self.bronnen.keys():
            parser.add_argument(
                f'--{key}', default=False,
                action='store_true', help=f'Load {key}')

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

        if options['indexgebied']:
            bag_fix.reindex_bag_buurt()

        target_dir = options['dir'] if options['dir'] is not None else '/data'
        log.info('Downloading / Importing from %s', target_dir)

        # import single bron
        for bron, import_function in self.bronnen.items():
            if options.get(bron):
                import_function(target_dir)
                return

        # if no aguments is given load ALL static sources
        for bron, import_function in self.bronnen.items():
                import_function(target_dir)
