from django.core.management.base import BaseCommand
from backend.Base_threlte_dv.models import Geometry
from django.db.models import Q

class Command(BaseCommand):
    help = 'Cleans up invalid model_url entries that point to .svelte files.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting to clean invalid model_url entries...'))

        # Find all geometries where model_url is not null and ends with .svelte
        invalid_geometries = Geometry.objects.filter(
            Q(model_url__isnull=False) & Q(model_url__endswith='.svelte')
        )

        count = invalid_geometries.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No invalid .svelte URLs found in model_url field. Database is clean.'))
            return

        self.stdout.write(f'Found {count} geometries with invalid .svelte URLs.')

        # Set model_url to None for these entries
        updated_count = invalid_geometries.update(model_url=None)

        self.stdout.write(self.style.SUCCESS(f'Successfully cleaned {updated_count} entries by setting model_url to null.'))
