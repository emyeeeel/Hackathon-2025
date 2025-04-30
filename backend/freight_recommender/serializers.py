from rest_framework import serializers
from .models import FreightType, ContainerType, LoadType, CargoCategory, FreightRecommendation

class FreightTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreightType
        fields = '__all__'

class ContainerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerType
        fields = '__all__'

class LoadTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadType
        fields = '__all__'

class CargoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoCategory
        fields = '__all__'

class FreightRecommendationSerializer(serializers.ModelSerializer):
    freight_type_details = FreightTypeSerializer(source='recommended_freight_type', read_only=True)
    container_type_details = ContainerTypeSerializer(source='recommended_container_type', read_only=True)
    load_type_details = LoadTypeSerializer(source='recommended_load_type', read_only=True)
    cargo_category_details = CargoCategorySerializer(source='cargo_category', read_only=True)

    class Meta:
        model = FreightRecommendation
        fields = '__all__'