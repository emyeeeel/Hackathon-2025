from rest_framework import serializers
from .models import Product

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

class ImageInputSerializer(serializers.Serializer):
    image = serializers.ImageField(required=False)
    image_url = serializers.URLField(required=False)

    def validate(self, data):
        if not data.get('image') and not data.get('image_url'):
            raise serializers.ValidationError("Either image or image_url must be provided.")
        return data