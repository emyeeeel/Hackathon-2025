from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FreightType, ContainerType, LoadType, CargoCategory

# Create your views here.
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

class FreightDataViewSet(APIView):
    def get(self, request):
        """Return all freight data for testing"""
        return Response({
            'freight_types': FreightTypeSerializer(FreightType.objects.all(), many=True).data,
            'container_types': ContainerTypeSerializer(ContainerType.objects.all(), many=True).data,
            'load_types': LoadTypeSerializer(LoadType.objects.all(), many=True).data,
            'cargo_categories': CargoCategorySerializer(CargoCategory.objects.all(), many=True).data
        })