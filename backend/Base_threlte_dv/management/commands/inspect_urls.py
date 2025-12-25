from django.core.management.base import BaseCommand
from backend.Base_threlte_dv.models import Geometry

class Command(BaseCommand):
    help = 'Inspects all model_url values in the Geometry table.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Inspecting model_url for all geometries...'))

        geometries = Geometry.objects.all().order_by('id')
        
        if not geometries.exists():
            self.stdout.write(self.style.SUCCESS('No geometries found in the database.'))
            return

        self.stdout.write('ID | Type | Model URL')
        self.stdout.write('------------------------------------')

        for geo in geometries:
            # Format the output to be clean
            geo_id = str(geo.id).ljust(3)
            geo_type = geo.type.ljust(15)
            model_url = geo.model_url if geo.model_url else "None"
            
            self.stdout.write(f'{geo_id}| {geo_type}| {model_url}')

        self.stdout.write(self.style.SUCCESS('\nInspection complete. Found ' + str(geometries.count()) + ' geometries.'))
