from rest_framework import serializers
from .models import Box, PackedBox, Product

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
            'id', 'length', 'width', 'height', 'weight', 'fill_capacity', 'volume'
        ]
class PackedBoxSerializer(serializers.ModelSerializer):
    box = BoxSerializer(read_only=True)
    total_weight = serializers.ReadOnlyField()
    volume_cbm = serializers.ReadOnlyField()
    category_type = serializers.ReadOnlyField()
    requires_refrigeration = serializers.ReadOnlyField()
    is_fragile = serializers.ReadOnlyField()

    class Meta:
        model = PackedBox
        fields = [
            'id', 'box', 'product', 'product_quantity', 'fill_percent',
            'total_weight', 'volume_cbm', 'category_type',
            'requires_refrigeration', 'is_fragile'
        ]