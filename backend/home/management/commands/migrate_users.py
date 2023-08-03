from django.core.management.base import BaseCommand
import argparse
import pandas as pd

class Command(BaseCommand):
    help = "Migrate Database"

    def add_arguments(self, parser):
         parser.add_argument('csvfile', nargs='?', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        data = pd.read_csv(options['csvfile'])
        print(data)