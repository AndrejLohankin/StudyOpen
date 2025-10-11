import csv
from django.core.management.base import BaseCommand
from phones.models import Phone
from datetime import datetime
from django.utils.text import slugify


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, nargs='?', default='phones.csv')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                release_date = datetime.strptime(row['release_date'], '%Y-%m-%d').date()
                lte = row['lte_exists'].lower() == 'true'
                Phone.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'price': row['price'],
                        'image': row['image'],
                        'release_date': release_date,
                        'lte_exists': lte,
                        'slug': row.get('slug', slugify(row['name']))
                    }
                )
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
