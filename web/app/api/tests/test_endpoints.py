import logging
import json
# import subprocess

# Packages
from rest_framework.test import APITestCase
from django.contrib.gis.geos import Polygon, MultiPolygon

from datasets.models.corporatie_bezit import GasAfwc2017
from datasets.models.bag import BagBuurt
from datasets.models.mip import Mip2016
from datasets.models.energie_labels import EnergieLabel
from datasets.models.renovaties import Renovatie
from datasets.models.handelsregister import Handelsregister
from datasets.models.handelsregister import HandelsregisterBuurt

from .factories import RenovatieFactory
from .factories import BuurtFactory
from .factories import BagRapportFactory
from .factories import CBSBuurtFactory
from .factories import GasAfwc2017Factory
from .factories import Mip2016Factory
from .factories import EnergieLabelFactory
from .factories import HandelsregisterFactory
from .factories import HandelsregisterBuurtFactory

from . import authorization

log = logging.getLogger(__name__)


def pretty_data(data):
    return json.dumps(data, indent=4, sort_keys=True)


VIERKANTJE = MultiPolygon([
    Polygon([
        (52.3733600, 4.8920225),
        (52.3733600, 4.8930556),
        (52.3728228, 4.8930556),
        (52.3728228, 4.8920225),
        (52.3733600, 4.8920225),
    ], srid=4326)
])


BINNNEN_VIERKANTJE = Polygon([
        (52.3733600, 4.8925225),
        (52.3733600, 4.8929556),
        (52.3729228, 4.8929556),
        (52.3729228, 4.8925225),
        (52.3733600, 4.8925225),
], srid=4326)

VIERKANTJE_VERWEG = Polygon([
        (53.3733600, 4.9920225),
        (53.3733600, 4.9930556),
        (53.3728228, 4.9930556),
        (53.3728228, 4.9920225),
        (53.3733600, 4.9920225),
], srid=4326)


class BrowseDatasetsTestCase(APITestCase, authorization.AuthorizationSetup):
    """
    Verifies that browsing the API works correctly.
    """

    datasets = [
        'gastransitie/api/afwc',
        'gastransitie/api/buurt',
        'gastransitie/api/energielabel',
        'gastransitie/api/renovatie',
        'gastransitie/api/mip',
        'gastransitie/api/bag',
        'gastransitie/api/buurtbbox',
        'gastransitie/api/handelsregister',
        'gastransitie/api/handelsregisterbuurt'
    ]

    def setUp(self):
        self.setUpAuthorization()
        super().setUpClass()

    @classmethod
    def setUpClass(cls):
        """
        This django app is merely a viewer on data
        we load testdata into database using special created
        """
        RenovatieFactory.create()
        cls.b1 = BuurtFactory.create(
            vollcode='ABCD',
            geometrie=VIERKANTJE
        )
        BagRapportFactory.create()
        CBSBuurtFactory.create()
        GasAfwc2017Factory.create()

        cls.m1 = Mip2016Factory.create(
            ogc_fid=1,
            wkb_geometry=BINNNEN_VIERKANTJE
        )

        cls.m2 = Mip2016Factory.create(
            ogc_fid=2,
            wkb_geometry=VIERKANTJE_VERWEG
        )

        EnergieLabelFactory.create()
        HandelsregisterFactory.create()
        HandelsregisterBuurtFactory.create()

    @classmethod
    def tearDownClass(cls):
        Renovatie.objects.all().delete()
        BagBuurt.objects.all().delete()
        GasAfwc2017.objects.all().delete()
        Mip2016.objects.all().delete()
        EnergieLabel.objects.all().delete()
        Handelsregister.objects.all().delete()
        HandelsregisterBuurt.objects.all().delete()

    def valid_response(self, url, response):
        """
        Helper method to check common status/json
        """

        self.assertEqual(
            200, response.status_code,
            'Wrong response code for {}'.format(url))

        self.assertEqual(
            'application/json', response['Content-Type'],
            'Wrong Content-Type for {}'.format(url))

    def valid_html_response(self, url, response):
        """
        Helper method to check common status/json
        """

        self.assertEqual(
            200, response.status_code,
            'Wrong response code for {}'.format(url))

        self.assertEqual(
            'text/html; charset=utf-8', response['Content-Type'],
            'Wrong Content-Type for {}'.format(url))

    def test_lists(self):
        for url in self.datasets:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(self.token_scope_gas))

            response = self.client.get('/{}/'.format(url))

            self.valid_response(url, response)

            self.assertIn(
                'count', response.data, 'No count attribute in {}'.format(url))
            self.assertNotEqual(
                response.data['count'],
                0, 'Wrong result count for {}'.format(url))

    def test_lists_html(self):
        for url in self.datasets:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(self.token_scope_gas))
            response = self.client.get('/{}/?format=api'.format(url))

            self.valid_html_response(url, response)

            self.assertIn(
                'count', response.data, 'No count attribute in {}'.format(url))

            self.assertNotEqual(
                response.data['count'],
                0, 'Wrong result count for {}'.format(url))

    def test_needs_auth(self):

        for url in self.datasets:

            response = self.client.get('/{}/?format=api'.format(url))
            self.assertEqual(response.status_code, 401, url)

    def test_filtering(self):
        """
        test buurt filtering
        """
        params = {'buurt': self.b1.vollcode}
        url = 'gastransitie/api/mip'
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(self.token_scope_gas))
        response = self.client.get(f'/{url}/', params)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
