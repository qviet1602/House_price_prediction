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
    expected_keys = ('id', 'year_month', 'list_price', 'created_date', 'modified_date', 'state', 'home_type')
    assert set(expected_keys).issubset(results[0].keys())
