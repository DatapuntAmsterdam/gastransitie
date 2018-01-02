from django.core.management.base import BaseCommand, CommandError

from datasets.imports import fix_tables


class Command(BaseCommand):
    help = 'Fix field types.'

    def handle(self, *args, **options):
        self.stdout.write('First stage of import process beginning:')
        self.stdout.write('(Assumes data files have been downloaded!')
        fix_tables.main()

        self.stdout.write('Done')
