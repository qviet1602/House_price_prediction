# -*- coding: utf-8 -*-

# Third Party Stuff
from django.db.models import Avg, F
from django_filters import rest_framework as filters

# domicilian Stuff
from domicilian.base import response
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

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


class AffordableCountiesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.AffordableCountiesSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("zipcode__state__name",)
    queryset = models.AnnualIncome.objects.all()

    def get_queryset(self):
        qs = self.queryset
        qs = qs.values("zipcode__county__name")
        qs = qs.annotate(
            avg_annual_income=Avg("avg_annual_income"),
            zipcode__state__name=F("zipcode__state__name"),
        )
        qs = qs.order_by("avg_annual_income")
        return qs


class PredictedPricesView(APIView):
    """
    A view that returns predicted prices for given `county_id`
    and `home_type_id`.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, format=None):

        county_name, home_type_id = (
            request.query_params.get("county_name", None),
            request.query_params.get("home_type_id", None),
        )
        if county_name and home_type_id:
            try:
                county_name, home_type_id = county_name, float(home_type_id)
            except ValueError:
                return response.BadRequest(
                    {"error": "county_name/home_type_id information is not correct."}
                )

            # The year and month are constantly 2020 and 9 repsectively for now.
            # TODO: Make this dynamic when we make this project
            # more dynamic

            county_obj = models.County.objects.filter(name__icontains=county_name).first()
            if not county_obj:
                return response.BadRequest({"error": "county_name is not correct."})
            county_id = county_obj.id

            instance = models.PredictedPrices.objects.filter(county_id=county_id, home_type_id=home_type_id).first()

            if not instance:
                return response.NoContent()
            serializer = serializers.PredictedPricesSerializer(instance)
            return response.Ok(serializer.data)

        return response.BadRequest(
            {"error": "county_name or home_type_id is not provided."}
        )
