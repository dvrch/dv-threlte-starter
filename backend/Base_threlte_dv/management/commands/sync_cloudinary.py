# backend/Base_threlte_dv/management/commands/sync_cloudinary.py

import cloudinary
import cloudinary.api
from django.conf import settings
from django.core.management.base import BaseCommand
from backend.Base_threlte_dv.models import CloudinaryAsset

class Command(BaseCommand):
    help = 'Synchronise la base de données locale avec les ressources de Cloudinary.'

    def handle(self, *args, **options):
        self.stdout.write('▶️  Démarrage de la synchronisation avec Cloudinary...')

        # La configuration de Cloudinary est déjà chargée depuis settings.py
        # Il n'est pas nécessaire de la reconfigurer ici.

        all_resources = []
        next_cursor = None

        try:
            self.stdout.write('.. Récupération des fichiers bruts (raw)...')
            while True:
                response = cloudinary.api.resources(
                    type="upload",
                    max_results=500,
                    next_cursor=next_cursor,
                    resource_type='raw'
                )
                all_resources.extend(response.get('resources', []))
                
                next_cursor = response.get('next_cursor')
                if not next_cursor:
                    break
            
            self.stdout.write('.. Récupération des images...')
            next_cursor = None # Reset cursor for the next resource type
            while True:
                response = cloudinary.api.resources(
                    type="upload", 
                    max_results=500, 
                    resource_type='image',
                    next_cursor=next_cursor
                )
                all_resources.extend(response.get('resources', []))

                next_cursor = response.get('next_cursor')
                if not next_cursor:
                    break

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'❌ Erreur lors de la communication avec l\'API Cloudinary: {e}'))
            return

        self.stdout.write(f'✅ {len(all_resources)} ressources trouvées sur Cloudinary. Début de la synchronisation avec la base de données.')

        synced_count = 0
        updated_count = 0
        for resource in all_resources:
            # update_or_create est parfait pour ça : il met à jour si l'objet existe, sinon il le crée.
            obj, created = CloudinaryAsset.objects.update_or_create(
                public_id=resource['public_id'],
                defaults={
                    'asset_id': resource['asset_id'],
                    'url': resource['secure_url'],
                    'asset_type': resource['resource_type'],
                    'file_name': resource.get('original_filename', resource['public_id']),
                    'format': resource.get('format', ''), # Utiliser .get() pour éviter les KeyError
                    'file_size': resource['bytes'],
                    'tags': resource.get('tags', []),
                }
            )
            if created:
                synced_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'🎉 Synchronisation terminée. {synced_count} nouvelles ressources ajoutées, {updated_count} ressources mises à jour.'))
