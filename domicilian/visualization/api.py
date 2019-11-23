# -*- coding: utf-8 -*-

# Third Party Stuff
from rest_framework import mixins
from rest_framework import serializers as rest_framework_serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# domicilian Stuff
from domicilian.base import response

from . import models, serializers


class StateMedianPricesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.StateMedianPricesSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()
    queryset = models.StateMedianPrice.objects.all()
