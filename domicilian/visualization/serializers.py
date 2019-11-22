# -*- coding: utf-8 -*-
# Third Party Stuff
from rest_framework import serializers

# domicillian Stuff
from .models import StateMedianPrice


class StateMedianPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateMedianPrice
        fields = "__all__"
