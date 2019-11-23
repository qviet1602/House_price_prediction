# Third Party Stuff
from django.test import TestCase
from django.test.client import RequestFactory

# domicilian Stuff
from domicilian.median_prices.views import *


class MedianPriceViewTestCase(TestCase):
    def test_list_medianprices(self):
        self.factory = RequestFactory()
        request = self.factory.get('/api/median_prices/')
        list_purchase_median_prices(request)

