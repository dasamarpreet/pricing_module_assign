from rest_framework import serializers

class PricingRequestSerializer(serializers.Serializer):
    distance = serializers.FloatField()
    ride_time = serializers.FloatField()
    waiting_time = serializers.FloatField()
    day_str = serializers.CharField(max_length=3)

