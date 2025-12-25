import json
import logging
import cloudinary.uploader
from rest_framework import serializers
from .models import Geometry, CloudinaryAsset
from .dv_config import TYPE_CHOICES

logger = logging.getLogger(__name__)

class GeometrySerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=TYPE_CHOICES, required=False)
    model_type = serializers.CharField(required=False, allow_blank=True)
    color_picker = serializers.CharField(write_only=True, required=False)
    model_file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Geometry
        fields = [
            'id', 'name', 'type', 'model_url', 'model_type',
            'position', 'rotation', 'scale', 'color', 'visible',
            'color_picker', 'model_file'
        ]

    def to_internal_value(self, data):
        # Multipart form data (QueryDict) sends everything as strings.
        if hasattr(data, "dict"):
            ret = data.dict()
        else:
            ret = data.copy()

        for field in ["position", "rotation", "scale"]:
            if field in ret and isinstance(ret[field], str):
                try:
                    val = ret[field].strip()
                    if val:
                        ret[field] = json.loads(val)
                except (json.JSONDecodeError, TypeError) as e:
                    logger.warning(f"Failed to parse JSON for field {field}: {val}")
        
        # Handle stringified booleans
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

    def handle_cloudinary_upload(self, model_file, validated_data):
        filename = model_file.name
        ext = filename.split('.')[-1].lower()
        
        is_image = ext in ['jpg', 'jpeg', 'png', 'webp', 'gif', 'svg']
        resource_type = 'image' if is_image else 'raw'
        folder = "dv-threlte/models"

        # Determine model_type and type based on extension
        if is_image:
            validated_data["type"] = "image_plane"
        elif ext in ["glb", "gltf"]:
            validated_data["type"] = "gltf_model"
        
        validated_data["model_type"] = ext

        upload_result = cloudinary.uploader.upload(
            model_file,
            folder=folder,
            resource_type=resource_type,
            public_id=filename.split('.')[0],
            overwrite=True,
            invalidate=True
        )
        return upload_result, resource_type, folder

    def create(self, validated_data):
        model_file = validated_data.pop("model_file", None)
        color_picker = validated_data.pop("color_picker", None)

        if color_picker:
            validated_data["color"] = color_picker

        if model_file:
            upload_result, resource_type, folder = self.handle_cloudinary_upload(model_file, validated_data)
            validated_data["model_url"] = upload_result["secure_url"]

        return Geometry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        model_file = validated_data.pop("model_file", None)
        color_picker = validated_data.pop("color_picker", None)

        if color_picker:
            instance.color = color_picker

        if model_file:
            upload_result, resource_type, folder = self.handle_cloudinary_upload(model_file, validated_data)
            instance.model_url = upload_result["secure_url"]
            instance.type = validated_data.get("type", instance.type)
            instance.model_type = validated_data.get("model_type", instance.model_type)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class CloudinaryAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudinaryAsset
        fields = '__all__'
