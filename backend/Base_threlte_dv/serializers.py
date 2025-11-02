from rest_framework import serializers
from .models import Geometry

class GeometrySerializer(serializers.ModelSerializer):
    color_picker = serializers.CharField(required=False)  # Champ pour le color picker

    class Meta:
        model = Geometry
        fields = '__all__'
        extra_kwargs = {
            'color': {'required': False},  # Rendre le champ 'color' non requis
            'color_picker': {'required': False},  # Rendre le champ 'color_picker' non requis
        }

    def validate_color(self, value):
        if not value.startswith('#'):
            value = '#' + value  # Ajoute '#' si absent
        return value

    def create(self, validated_data):
        # Si 'color_picker' est fourni, utilisez-le pour définir la couleur
        if 'color_picker' in validated_data:
            validated_data['color'] = validated_data.pop('color_picker')
        return super().create(validated_data)  # Appel à la méthode de création par défaut

