"""
Helpers to create dynamic model instances for testing purposes.

Usages:
>>> from tests import factories as f
>>>
>>> user = f.create_user(first_name="Robert", last_name="Downey")  # creates single instance of user
>>> users = f.create_user(n=5, is_active=False)  # creates 5 instances of user

There is a bit of magic going on behind the scenes with `G` method from https://django-dynamic-fixture.readthedocs.io/
"""

# Third Party Stuff
from django.apps import apps
from django.conf import settings
from django_dynamic_fixture import G


def create_user(**kwargs):
    """Create an user along with their dependencies."""
    User = apps.get_model(settings.AUTH_USER_MODEL)
    user = G(User, **kwargs)
    user.set_password(kwargs.get("password", "test"))
    user.save()
    return user


def create_state(**kwargs):
    return G(apps.get_model("visualization", 'State'), **kwargs)


def create_state_median_prices(**kwargs):
    if not kwargs.get("state"):
        state = create_state()
        kwargs["state_code"] = state
    return G(apps.get_model("visualization", 'StateMedianPrice'), **kwargs)


def create_county(**kwargs):
    return G(apps.get_model("visualization", "County"), **kwargs)


def create_city(**kwargs):
    return G(apps.get_model("visualization", "City"), **kwargs)


def create_zip_code(**kwargs):
    state = create_state()
    kwargs["state"] = state
    county = create_county()
    kwargs["county"] = county
    city = create_city()
    kwargs["city"] = city
    return G(apps.get_model("visualization", "ZipCode"), **kwargs)


def create_annual_income(**kwargs):
    # zipcode = create_zip_code()
    # kwargs["zipcode"] = zipcode
    return G(apps.get_model("visualization", "AnnualIncome"), **kwargs)


def create_crime_data(**kwargs):
    zipcode = create_zip_code()
    kwargs["zipcode"] = zipcode
    return G(apps.get_model("visualization", "CrimeData"), **kwargs)


def create_predicted_prices(**kwargs):
    return G(apps.get_model("visualization", "PredictedPrices"), **kwargs)
