# -*- coding: utf-8 -*-
# Third Party Stuff
from rest_framework import serializers

# domicillian Stuff
from .models import CrimeData, StateMedianPrice


class StateMedianPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateMedianPrice
        fields = "__all__"


class CrimeRateSerializer(serializers.Serializer):
    county = serializers.CharField(source="zipcode__county__name")
    state = serializers.CharField(source="zipcode__state__name")
    avg_crime_rate = serializers.FloatField()

    class Meta:
        model = CrimeData
        fields = ("county", "avg_crime_rate", "state")
