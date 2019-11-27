# -*- coding: utf-8 -*-
# Third Party Stuff
from rest_framework import serializers

# domicillian Stuff
from .models import CrimeData, StateMedianPrice, PredictedPrices


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


class AffordableCountiesSerializer(serializers.Serializer):
    county = serializers.CharField(source="zipcode__county__name")
    state = serializers.CharField(source="zipcode__state__name")
    avg_annual_income = serializers.FloatField()

    class Meta:
        model = CrimeData
        fields = ("county", "avg_annual_income", "state")


class PredictedPricesSerializer(serializers.ModelSerializer):
    predicted_price = serializers.FloatField(source="y_pred")

    class Meta:
        model = PredictedPrices
        fields = ("county_id", "predicted_price", "home_type_id")
