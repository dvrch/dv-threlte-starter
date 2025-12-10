from rest_framework import serializers
from .models import Geometry, CloudinaryAsset, B2Asset


class GeometrySerializer(serializers.ModelSerializer):
    model_file = serializers.FileField(write_only=True, required=False, allow_null=True)
    model_url = serializers.SerializerMethodField(read_only=True)
    color_picker = serializers.CharField(
        write_only=True, required=False
    )  # Réintroduit le champ color_picker

    class Meta:
        model = Geometry
        fields = [
            "id",
            "type",
            "name",
            "model_file",
            "model_url",
            "model_type",
            "position",
            "rotation",
            "color",
            "cloudinary_asset",
            "b2_asset",
            "color_picker",  # Ajout de color_picker
        ]
        read_only_fields = ["cloudinary_asset", "b2_asset"]

    def get_model_url(self, obj):
        """Return the appropriate URL based on available asset"""
        if obj.b2_asset:
            return obj.b2_asset.url
        elif obj.cloudinary_asset:
            return obj.cloudinary_asset.url
        elif obj.model_file:
            return obj.model_file.url
        return None

    def validate_color(self, value):  # Réintroduit la validation de couleur
        if value and not value.startswith("#"):
            value = "#" + value
        return value

    def create(self, validated_data):
        model_file = validated_data.pop("model_file", None)
        color_picker = validated_data.pop("color_picker", None)  # Gérer color_picker

        if color_picker:
            validated_data["color"] = color_picker

        # Créer l'instance Geometry sans le fichier pour l'instant
        from .models import Geometry

        geometry_instance = Geometry.objects.create(**validated_data)

        if model_file:
            # Assigner le fichier à l'instance, ce qui déclenche l'upload Cloudinary
            geometry_instance.model_file = model_file
            geometry_instance.save()  # Sauvegarde pour que model_file soit traité

            # Après la sauvegarde, model_file.public_id et .url sont disponibles
            if hasattr(geometry_instance.model_file, "public_id"):
                from .models import CloudinaryAsset

                asset, created = CloudinaryAsset.objects.update_or_create(
                    public_id=geometry_instance.model_file.public_id,
                    defaults={
                        "asset_id": getattr(
                            geometry_instance.model_file, "asset_id", None
                        ),
                        "url": geometry_instance.model_file.url,
                        "asset_type": "raw",
                        "file_name": geometry_instance.model_file.name,
                        "file_size": geometry_instance.model_file.size,
                    },
                )
                geometry_instance.cloudinary_asset = asset
                geometry_instance.save(
                    update_fields=["cloudinary_asset"]
                )  # Sauvegarder la liaison

        return geometry_instance

    def update(self, instance, validated_data):
        model_file = validated_data.pop("model_file", None)
        color_picker = validated_data.pop("color_picker", None)  # Gérer color_picker

        if color_picker:
            validated_data["color"] = color_picker

        # Mettre à jour les champs de l'instance Geometry
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if model_file:
            instance.model_file = model_file
            instance.save()  # Sauvegarde pour que model_file soit traité

            if hasattr(instance.model_file, "public_id"):
                from .models import CloudinaryAsset

                asset, created = CloudinaryAsset.objects.update_or_create(
                    public_id=instance.model_file.public_id,
                    defaults={
                        "asset_id": getattr(instance.model_file, "asset_id", None),
                        "url": instance.model_file.url,
                        "asset_type": "raw",
                        "file_name": instance.model_file.name,
                        "file_size": instance.model_file.size,
                    },
                )
                instance.cloudinary_asset = asset
                instance.save(update_fields=["cloudinary_asset"])
        else:
            instance.save()  # Sauvegarder les autres modifications si pas de fichier

        return instance


class B2AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2Asset
        fields = "__all__"
