# Standard Library
from datetime import timedelta

# Third Party Stuff
import pytest
from django.urls import reverse
from django.utils import timezone

# domicilian Stuff
from domicilian.visualization import models

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_state_median_prices_api(client, mocker):
    f.create_state_median_prices(n=5)
    url = reverse("state_median_prices-list")
    response = client.json.get(url)
    assert response.status_code == 200
    results = response.data["results"]
    assert len(results) == 5
    expected_keys = (
        "id",
        "year_month",
        "list_price",
        "created_date",
        "modified_date",
        "state",
        "home_type",
    )
    assert set(expected_keys).issubset(results[0].keys())


def test_crime_rate_api(client):
    f.create_crime_data()
    url = reverse("crime_rate-list")
    response = client.json.get(url)
    assert response.status_code == 200
    results = response.data["results"]
    assert len(results) == 1
    expected_keys = ("county", "state", "avg_crime_rate")
    assert set(expected_keys).issubset(results[0].keys())


def test_affordable_api(client):
    f.create_annual_income()
    url = reverse("affordable_counties-list")
    response = client.json.get(url)
    assert response.status_code == 200
    results = response.data["results"]
    assert len(results) == 1
    expected_keys = ("county", "state", "avg_annual_income")
    assert set(expected_keys).issubset(results[0].keys())


def test_predicted_prices_api_with_no_query_param(client):
    url = reverse("predicted-prices")
    response = client.json.get(url)
    assert response.status_code == 400
    assert response.data["error"] == "county_name or home_type_id is not provided."


def test_predicted_prices_api_with_valid_data(client):
    county = f.create_county(name="Clayton")
    f.create_predicted_prices(county_id=county.id, home_type_id=3, y_pred=12342.40)
    url = reverse("predicted-prices") + "?county_name=clayton&home_type_id=3"
    response = client.json.get(url)
    assert response.status_code == 200
    expected_keys = ("county_id", "home_type_id", "predicted_price")
    assert set(expected_keys).issubset(response.data.keys())


def test_predicted_prices_api_when_county_name_is_not_correct(client):
    url = reverse("predicted-prices") + "?county_name=1&home_type_id=1"
    response = client.json.get(url)
    assert response.status_code == 400
    assert response.data["error"] == "county_name is not correct."


def test_predicted_prices_api_when_predicted_price_not_available(client):
    county = f.create_county(name="Clayton")
    url = reverse("predicted-prices") + "?county_name=clayton&home_type_id=1"
    response = client.json.get(url)
    assert response.status_code == 204
