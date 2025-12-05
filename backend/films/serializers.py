from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from .models import Film


class FilmSerializer(TaggitSerializer, serializers.ModelSerializer):
    image_url = serializers.URLField(max_length=1024, required=False, allow_blank=True)
    tags = TagListSerializerField(default=[])

    class Meta:
        model = Film
        fields = ("id", "name", "director", "description", "image_url", "tags")
