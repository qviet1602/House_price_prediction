# -*- coding: utf-8 -*-
"""Root url routering file.

You should put the url config in their respective app putting only a
refernce to them here.
"""

# Third Party Stuff
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path, re_path

from . import api_urls
from .base import views as base_views
from .base.api import schemas as api_schemas
from .median_prices.views import *
from .visualization.views import *

admin.site.site_title = admin.site.site_header = "domicilian Administration"
handler500 = base_views.server_error

# Top Level Pages
# ==============================================================================
urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path("map/", TemplateView.as_view(template_name="pages/map.html"), name="map"),
    path("visualize/", TemplateView.as_view(template_name="pages/graph.html"), name="visualize"),
    path("trends_by_state_purchase/", TemplateView.as_view(template_name="pages/trends_by_state_purchase.html"), name="trends_by_state_purchase"),
    path("trends_by_state_rental/", TemplateView.as_view(template_name="pages/trends_by_state_rental.html"), name="trends_by_state_rental"),
    path("trends_by_county_purchase/", TemplateView.as_view(template_name="pages/trends_by_county_purchase.html"), name="trends_by_county_purchase"),
    path("trends_by_county_rental/", TemplateView.as_view(template_name="pages/trends_by_county_rental.html"), name="trends_by_county_rental"),
    path("trends_by_zip_purchase/", TemplateView.as_view(template_name="pages/trends_by_zip_purchase.html"), name="trends_by_zip_purchase"),
    path("graphical_visualization/", TemplateView.as_view(template_name="pages/slippymap.html"), name="graphical_visualization"),
    path("api/purchase_median_prices/", list_purchase_median_prices),
    path("api/rental_median_prices/", list_rental_median_prices),
    path("api/list_states/", list_states),
    path("api/list_counties_purchase/", list_counties_purchase),
    path("api/list_counties_rental/", list_counties_rental),
    path("api/list_zips_purchase/", list_zips_purchase),
    path("api/county_data_purchase/", get_county_data_purchase),
    path("api/county_data_rental/", get_county_data_rental),
    path("api/zip_data_purchase/", get_zip_data_purchase),
    path("api/state_data_purchase/", get_state_data_purchase),
    path("api/state_data_rental/", get_state_data_rental),
    path("api/node_stats/", get_node_stats),
    path("api/best_counties/", get_best_counties),
    path("api/best_zips/", get_best_zips),
    path("api/safe_counties/", get_safe_counties),
    path("api/affordable/", get_affordable_counties),
    path("api/similar_states/", get_similar_states),
    path("api/similar_all/", get_similar_all),
    path("api/all_data/", get_all_data)
    # Your stuff: custom urls go here
]

urlpatterns += [
    re_path(
        r"^(?P<filename>(robots.txt)|(humans.txt))$",
        base_views.root_txt_files,
        name="root-txt-files",
    ),
    # Rest API
    path("api/", include(api_urls)),
    # Django Admin
    path("{}/".format(settings.DJANGO_ADMIN_URL), admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.API_DEBUG:
    urlpatterns += [
        # Browsable API
        path("schema/", api_schemas.schema_view, name="schema"),
        path("api-playground/", api_schemas.swagger_schema_view, name="api-playground"),
        path("api/auth-n/", include("rest_framework.urls", namespace="rest_framework")),
    ]

if settings.DEBUG:
    from django.views import defaults as dj_default_views
    from django.urls import get_callable

    urlpatterns += [
        path(
            "400/",
            dj_default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            dj_default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied!")},
        ),
        path("403_csrf/", get_callable(settings.CSRF_FAILURE_VIEW)),
        path(
            "404/",
            dj_default_views.page_not_found,
            kwargs={"exception": Exception("Not Found!")},
        ),
        path("500/", handler500),
    ]

    # Django Debug Toolbar
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
