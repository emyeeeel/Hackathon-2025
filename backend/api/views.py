from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Product
import requests
from django.conf import settings
from .serializers import ImageInputSerializer, ProductSerializer
from .utils import process_image_input, check_product_match

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DetectProductView(APIView):
    def post(self, request):
        serializer = ImageInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get image input (file or URL)
        image = serializer.validated_data.get('image')
        image_url = serializer.validated_data.get('image_url')
        image_input = image if image else image_url

        try:
            # Process image input
            image_payload = process_image_input(image_input)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare Roboflow request
        payload = {
            "api_key": settings.ROBOFLOW_API_KEY,
            "inputs": {"image": image_payload}
        }

        try:
            # Send to Roboflow
            response = requests.post(
                "https://serverless.roboflow.com/infer/workflows/hackathon-idqc5/custom-workflow-2",
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            # Extract detection results
            detected_class = data["outputs"][0]["predictions"]["predictions"][0]["class"]
            product = check_product_match(detected_class)

            # Prepare response
            response_data = {
                "detected_class": detected_class,
                "product": ProductSerializer(product).data if product else None
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Roboflow request failed: {str(e)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except KeyError as e:
            return Response({"error": f"Invalid response format: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)