from rest_framework import serializers
from .models import Box, Product

class ProductSerializer(serializers.ModelSerializer):
    total_weight = serializers.ReadOnlyField()  # Read-only field for the calculated property

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'subcategory',
            'width', 'height', 'length', 'weight', 'quantity',
            'is_fragile', 'requires_refrigeration', 'expiration_date',
            'created_at', 'updated_at', 'total_weight'
        ]


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = [
            'id', 'length', 'width', 'height', 'fill_capacity', 'volume'
        ]