from rest_framework import serializers
from .models import Geometry, CloudinaryAsset

class GeometrySerializer(serializers.ModelSerializer):
    model_file = serializers.FileField(write_only=True, required=False, allow_null=True)
    model_url = serializers.URLField(source='asset.url', read_only=True)
    color_picker = serializers.CharField(write_only=True, required=False) # Réintroduit le champ color_picker

    class Meta:
        model = Geometry
        fields = [
            'id', 'type', 'name', 'model_file', 'model_url', 'model_type', 
            'position', 'rotation', 'color', 'asset', 'color_picker' # Ajout de color_picker
        ]
        read_only_fields = ['asset']

    def validate_color(self, value): # Réintroduit la validation de couleur
        if value and not value.startswith('#'):
            value = '#' + value
        return value

    def create(self, validated_data):
        model_file = validated_data.pop('model_file', None)
        color_picker = validated_data.pop('color_picker', None) # Gérer color_picker

        if color_picker:
            validated_data['color'] = color_picker

        # Créer l'instance Geometry sans le fichier pour l'instant
        geometry_instance = Geometry.objects.create(**validated_data)

if model_file:
            # Assigner le fichier à l'instance, ce qui déclenche l'upload Cloudinary
            geometry_instance.model_file = model_file
            geometry_instance.save() # Sauvegarde pour que model_file soit traité

            # Debug: Check what attributes are available
            print(f"DEBUG: model_file = {geometry_instance.model_file}")
            print(f"DEBUG: hasattr public_id: {hasattr(geometry_instance.model_file, 'public_id')}")
            print(f"DEBUG: hasattr url: {hasattr(geometry_instance.model_file, 'url')}")
            if hasattr(geometry_instance.model_file, 'url'):
                print(f"DEBUG: url = {geometry_instance.model_file.url}")

            # Après la sauvegarde, model_file.public_id et .url sont disponibles
            if hasattr(geometry_instance.model_file, 'public_id'):
asset, created = CloudinaryAsset.objects.update_or_create(
                    public_id=geometry_instance.model_file.public_id,
                    defaults={
                        'asset_id': getattr(geometry_instance.model_file, 'asset_id', None),
                        'url': geometry_instance.model_file.url,
                        'asset_type': 'raw',
                        'file_name': geometry_instance.model_file.name,
                        'file_size': geometry_instance.model_file.size,
                    }
                )
                geometry_instance.asset = asset
                geometry_instance.save(update_fields=['asset']) # Sauvegarder la liaison

        return geometry_instance

    def update(self, instance, validated_data):
        model_file = validated_data.pop('model_file', None)
        color_picker = validated_data.pop('color_picker', None) # Gérer color_picker

        if color_picker:
            validated_data['color'] = color_picker

        # Mettre à jour les champs de l'instance Geometry
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if model_file:
            instance.model_file = model_file
            instance.save() # Sauvegarde pour que model_file soit traité

            if hasattr(instance.model_file, 'public_id'):
                asset, created = CloudinaryAsset.objects.update_or_create(
                    public_id=instance.model_file.public_id,
                    defaults={
                        'asset_id': getattr(instance.model_file, 'asset_id', None),
                        'url': instance.model_file.url,
                        'asset_type': 'raw',
                        'file_name': instance.model_file.name,
                        'file_size': instance.model_file.size,
                    }
                )
                instance.asset = asset
                instance.save(update_fields=['asset'])
        else:
            instance.save() # Sauvegarder les autres modifications si pas de fichier

        return instance

