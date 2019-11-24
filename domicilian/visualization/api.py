# -*- coding: utf-8 -*-

# Third Party Stuff
from django.db.models import Avg, F
from django_filters import rest_framework as filters

# domicilian Stuff
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from . import models, serializers


class StateMedianPricesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.StateMedianPricesSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()
    queryset = models.StateMedianPrice.objects.all()


class CrimeRateViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CrimeRateSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("zipcode__state__name",)
    queryset = models.CrimeData.objects.all()

    def get_queryset(self):
        qs = self.queryset
        qs = qs.values("zipcode__county__name")
        qs = qs.annotate(
            avg_crime_rate=Avg("violent_crime"),
            zipcode__state__name=F("zipcode__state__name"),
        )
        qs = qs.order_by("avg_crime_rate")
        return qs
