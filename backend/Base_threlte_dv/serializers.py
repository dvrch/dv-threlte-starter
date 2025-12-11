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
    color_picker = serializers.CharField(
        write_only=True, required=False
    )

    class Meta:
        model = Geometry
        fields = [
            "id",
            "type",
            "name",
            "model_file", # For upload
            "model_url",  # For download/display
            "model_type",
            "position",
            "rotation",
            "color",
            "color_picker",
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
            # Manually upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                model_file,
                resource_type="raw",
                folder="dv-threlte/models" # Specify the folder
            )
            # Add the full URL to the data to be saved
            validated_data['model_url'] = upload_result['secure_url']

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
            upload_result = cloudinary.uploader.upload(
                model_file,
                resource_type="raw",
                folder="dv-threlte/models"
            )
            # Update the instance's model_url with the new URL
            instance.model_url = upload_result['secure_url']

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
