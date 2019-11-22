from rest_framework import serializers
from .models import MedianPrice

class MedianPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedianPrice
        fields = ("name", "state_code", "list_price")