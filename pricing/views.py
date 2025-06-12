from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import calculate_price
from .serializers import PricingRequestSerializer

class CalculatePriceView(APIView):
    def post(self, request):
        serializer = PricingRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Extract values
                distance = serializer.validated_data['distance']
                ride_time = serializer.validated_data['ride_time']
                waiting_time = serializer.validated_data['waiting_time']
                day_str = serializer.validated_data['day_str']
                
                # Calculate price using the function
                price = calculate_price(distance, ride_time, waiting_time, day_str)
                return Response({'price': price}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)
