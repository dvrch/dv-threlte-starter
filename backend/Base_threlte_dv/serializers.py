import logging
import json
import re
import cloudinary.uploader
from rest_framework import serializers
from .models import Geometry, CloudinaryAsset

logger = logging.getLogger(__name__)

class GeometrySerializer(serializers.ModelSerializer):
    model_file = serializers.FileField(write_only=True, required=False, allow_null=True)
    model_url = serializers.URLField(read_only=True)
    color_picker = serializers.CharField(write_only=True, required=False)

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
            "scale",
            "color",
            "color_picker",
            "visible",
        ]

    def to_internal_value(self, data):
        # Multipart form data (QueryDict) sends everything as strings.
        # We must convert to a mutable dict and parse JSON fields.
        if hasattr(data, "dict"):
            ret = data.dict()
        else:
            ret = data.copy()

        for field in ["position", "rotation", "scale"]:
            if field in ret and isinstance(ret[field], str):
                try:
                    # Clean the string in case of extra quotes or escaping
                    val = ret[field].strip()
                    if val:
                        ret[field] = json.loads(val)
                except (json.JSONDecodeError, TypeError) as e:
                    logger.warning(f"Failed to parse JSON for field {field}: {val}. Error: {e}")
                    # Let it pass, the serializer will catch the validation error if invalid
                    pass
        
        # Handle stringified booleans from FormData
        if "visible" in ret and isinstance(ret["visible"], str):
            val = ret["visible"].lower()
            if val == "true":
                ret["visible"] = True
            elif val == "false":
                ret["visible"] = False

        return super().to_internal_value(ret)

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
            # Detect extension
            ext = model_file.name.split(".")[-1].lower()
            
            # If a file is uploaded, determine its type
            if ext in ["glb", "gltf"]:
                validated_data["type"] = "gltf_model"
                validated_data["model_type"] = ext
                resource_type = "raw"
            elif ext in ["jpg", "jpeg", "png", "webp"]:
                validated_data["type"] = "image_plane"
                validated_data["model_type"] = ext
                resource_type = "image"
            else:
                validated_data["type"] = "gltf_model"
                validated_data["model_type"] = ext
                resource_type = "raw"

            upload_result = cloudinary.uploader.upload(
                model_file,
                resource_type=resource_type,
                folder="dv-threlte/models",
                # We can use the original filename for the public_id to keep it readable
                use_filename=True,
                unique_filename=False,  # If a file with the same name exists, it will be overwritten.
                overwrite=True,
            )
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

            # Detect extension
            ext = model_file.name.split(".")[-1].lower()
            
            # If a file is uploaded, determine its type
            if ext in ["glb", "gltf"]:
                validated_data["type"] = "gltf_model"
                validated_data["model_type"] = ext
                resource_type = "raw"
            elif ext in ["jpg", "jpeg", "png", "webp"]:
                validated_data["type"] = "image_plane"
                validated_data["model_type"] = ext
                resource_type = "image"
            else:
                validated_data["type"] = "gltf_model"
                validated_data["model_type"] = ext
                resource_type = "raw"

            upload_result = cloudinary.uploader.upload(
                model_file,
                resource_type=resource_type,
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
