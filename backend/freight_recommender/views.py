from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import FreightType, ContainerType, LoadType, CargoCategory, FreightRecommendation
from .serializers import (FreightTypeSerializer, ContainerTypeSerializer, LoadTypeSerializer, CargoCategorySerializer, FreightRecommendationSerializer)
from .services import FreightRecommendationService


# Create your views here.

# Standard CRUD viewsets for reference data
class FreightTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FreightType.objects.all()
    serializer_class = FreightTypeSerializer

class ContainerTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContainerType.objects.all()
    serializer_class = ContainerTypeSerializer

class LoadTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LoadType.objects.all()
    serializer_class = LoadTypeSerializer

class CargoCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargoCategory.objects.all()
    serializer_class = CargoCategorySerializer

# Data viewset for testing purposes
class FreightDataView(APIView):
    def get(self, request):
        """Return all freight data for testing"""
        return Response({
            'freight_types': FreightTypeSerializer(FreightType.objects.all(), many=True).data,
            'container_types': ContainerTypeSerializer(ContainerType.objects.all(), many=True).data,
            'load_types': LoadTypeSerializer(LoadType.objects.all(), many=True).data,
            'cargo_categories': CargoCategorySerializer(CargoCategory.objects.all(), many=True).data
        })
    
# Recommendation API
class FreightRecommendationView(APIView):
    """ Generate freight recommendations based on cargo specifications """

    def post(self, request):
        try:
            #Validate the input
            required_fields = ['cargo_weight_kg', 'cargo_volume_cubic_m', 'cargo_category_id']
            for field in required_fields:
                if field not in request.data:
                    return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)
                
            # Get a recommendation
            recommendation = FreightRecommendationService.recommend_freight(
                cargo_weight_kg=float(request.data['cargo_weight_kg']),
                cargo_volume_cubic_m=float(request.data['cargo_volume_cubic_m']),
                cargo_category_id=int(request.data['cargo_category_id']),
                destination_type=request.data.get('destination_type', 'domestic')
            )

            if not recommendation:
                return Response({"error": "Unable to generate recommendation"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Save recommendation to database for logging / analysis purposes
            recommendation_record = FreightRecommendation.objects.create(
                cargo_weight_kg=float(request.data['cargo_weight_kg']),
                cargo_volume_cubic_m=float(request.data['cargo_volume_cubic_m']),
                cargo_category_id=int(request.data['cargo_category_id']),
                recommended_freight_type=recommendation['freight_type'],
                recommended_container_type=recommendation['container_type'],
                recommended_load_type=recommendation['load_type'],
                additional_notes=recommendation['notes']
            )

            # Returning result
            return Response({
                "recommendation_id": recommendation_record.id,
                "freight_type": FreightTypeSerializer(recommendation['freight_type']).data,
                "container_type": ContainerTypeSerializer(recommendation['container_type']).data if recommendation['container_type'] else None,
                "load_type": LoadTypeSerializer(recommendation['load_type']).data,
                "additional_notes": recommendation['notes']
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

