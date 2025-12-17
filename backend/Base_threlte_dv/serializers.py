from rest_framework import serializers
from .models import Geometry, CloudinaryAsset


import cloudinary.uploader
from rest_framework import serializers
from .models import Geometry, CloudinaryAsset


class GeometrySerializer(serializers.ModelSerializer):
    model_file = serializers.FileField(write_only=True, required=False, allow_null=True)
    # model_url is now a direct field of the model, so no 'source' is needed.
    # It will be read-only during serialization, but we'll set it manually in create/update.
    model_url = serializers.URLField(read_only=True)
    color_picker = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Geometry
        fields = [
            "id",
            "type",
            "name",
            "model_file",  # For upload
            "model_url",  # For download/display
            "model_type",
            "position",
            "rotation",
            "scale",  # Added scale field
            "color",
            "color_picker",
            "visible",
        ]

    def validate_color(self, value):
        if value and not value.startswith("#"):
            value = "#" + value
        return value

    def create(self, validated_data):
        model_file = validated_data.pop("model_file", None)
        color_picker = validated_data.pop("color_picker", None)

        if color_picker:
            validated_data["color"] = color_picker

        if model_file:
            # Disable Cloudinary versioning and use sequential naming
            import os
            from django.db.models import Max

            # Get count for naming
            max_id = Geometry.objects.all().aggregate(Max("id"))["id__max"] or 0
            next_id = (max_id + 1) if max_id else 1

            # Generate simple filename
            filename = f"upload_{next_id}.glb"

            upload_result = cloudinary.uploader.upload(
                model_file,
                resource_type="raw",
                folder="dv-threlte/models",
                public_id=filename,  # Use our naming
                use_filename=True,  # Disable versioning
                unique_filename=False,  # Allow overwrite
                overwrite=True,  # Allow overwriting existing files
            )
            # Add the full URL to data to be saved
            validated_data["model_url"] = upload_result["secure_url"]

        # Create the Geometry instance
        geometry_instance = Geometry.objects.create(**validated_data)
        return geometry_instance

    def update(self, instance, validated_data):
        model_file = validated_data.pop("model_file", None)
        color_picker = validated_data.pop("color_picker", None)

        if color_picker:
            validated_data["color"] = color_picker

        if model_file:
            # If there's a new file, upload it
            # First, delete the old Cloudinary asset if it exists
            if instance.model_url:
                try:
                    # Extract public_id from the old model_url
                    import re

                    url_pattern = r"/dv-threlte/models/([^/]+)"
                    match = re.search(url_pattern, instance.model_url)
                    if match:
                        old_public_id = f"dv-threlte/models/{match.group(1)}"
                        cloudinary.uploader.destroy(old_public_id, resource_type="raw")
                        # Delete the old CloudinaryAsset record
                        CloudinaryAsset.objects.filter(public_id=old_public_id).delete()
                        print(
                            f"✅ Deleted old Cloudinary asset and record: {old_public_id}"
                        )
                    else:
                        print(
                            f"⚠️ Could not extract public_id from old model_url: {instance.model_url}. Old Cloudinary asset not deleted."
                        )
                except Exception as e:
                    print(f"❌ Error deleting old Cloudinary asset: {str(e)}")

            upload_result = cloudinary.uploader.upload(
                model_file,
                resource_type="raw",
                folder="dv-threlte/models",
                use_filename=True,  # Disable versioning
                unique_filename=False,  # Allow overwrite
            )
            # Update the instance's model_url with the new URL
            instance.model_url = upload_result["secure_url"]

            # Create or update the CloudinaryAsset record for the new file
            new_public_id = upload_result["public_id"]
            CloudinaryAsset.objects.update_or_create(
                public_id=new_public_id,
                defaults={
                    "url": upload_result["secure_url"],
                    "asset_type": "raw",
                    "file_name": instance.name or new_public_id.split("/")[-1],
                    "file_size": upload_result.get("bytes", 0),
                    "format": upload_result.get("format", ""),
                },
            )
            print(f"✅ Created/Updated CloudinaryAsset for new file: {new_public_id}")

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
