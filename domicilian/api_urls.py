# Third Party Stuff
from rest_framework.routers import DefaultRouter

# domicilian Stuff
from domicilian.base.api.routers import SingletonRouter
from domicilian.users.api import CurrentUserViewSet
from domicilian.users.auth.api import AuthViewSet

default_router = DefaultRouter(trailing_slash=False)
singleton_router = SingletonRouter(trailing_slash=False)

# Register all the django rest framework viewsets below.
default_router.register("auth", AuthViewSet, basename="auth")
singleton_router.register("me", CurrentUserViewSet, basename="me")

# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = default_router.urls + singleton_router.urls
