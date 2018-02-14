"""
Download datasets from objectstore, save them in local directory.
"""
import os

from django.core.management.base import BaseCommand, CommandError

from datasets.imports import download_datafiles


class Command(BaseCommand):
    help = 'Download gastransitie data files from object store.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir', dest='dir', type=str,
            help='Directory to store the datafiles (default /data).')

    def handle(self, *args, **options):
        self.stdout.write('Downloading datafiles from objectstore.')
        target_dir = options['dir'] if options['dir'] is not None else '/data'
        download_datafiles.main(target_dir)
        self.stdout.write('Done')
