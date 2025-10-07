from rest_framework import serializers
from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for Recipe model.
    """
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'cuisine',
            'rating',
            'prep_time',
            'cook_time',
            'total_time',
            'description',
            'nutrients',
            'serves',
            'continent',
            'country_state',
            'url',
            'ingredients',
            'instructions',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
