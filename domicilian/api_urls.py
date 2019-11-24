# Third Party Stuff
# domicilian Stuff
from domicilian.base.api.routers import SingletonRouter
from domicilian.users.api import CurrentUserViewSet
from domicilian.users.auth.api import AuthViewSet
from domicilian.visualization.api import CrimeRateViewSet, StateMedianPricesViewSet
from rest_framework.routers import DefaultRouter

default_router = DefaultRouter(trailing_slash=False)
singleton_router = SingletonRouter(trailing_slash=False)

# Register all the django rest framework viewsets below.
default_router.register("auth", AuthViewSet, basename="auth")
singleton_router.register("me", CurrentUserViewSet, basename="me")
default_router.register(
    "state_median_prices", StateMedianPricesViewSet, basename="state_median_prices"
)
default_router.register("crime_rate", CrimeRateViewSet, basename="crime_rate")

# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = default_router.urls + singleton_router.urls
