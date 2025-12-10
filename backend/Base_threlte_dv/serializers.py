from rest_framework import serializers
from .models import Geometry, CloudinaryAsset

class GeometrySerializer(serializers.ModelSerializer):
    model_file = serializers.FileField(write_only=True, required=False, allow_null=True)
    # model_url est maintenant un champ en lecture seule qui expose l'URL de l'asset lié.
    model_url = serializers.URLField(source='asset.url', read_only=True)

    class Meta:
        model = Geometry
        # On expose 'model_url' qui est maintenant en lecture seule
        fields = [
            'id', 'type', 'name', 'model_file', 'model_url', 'model_type', 
            'position', 'rotation', 'color', 'asset'
        ]
        read_only_fields = ['asset'] # Le champ 'asset' sera géré par la vue, pas directement par le client.

