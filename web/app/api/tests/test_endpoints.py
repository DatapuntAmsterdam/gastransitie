import logging
import json
# import subprocess

# Packages
from rest_framework.test import APITestCase

from datasets.models.corporatie_bezit import GasAfwc2017
from datasets.models.bag import BagBuurt
from datasets.models.mip import Mip2016
from datasets.models.energie_labels import EnergieLabel
from datasets.models.renovaties import Renovatie

from .factories import RenovatieFactory
from .factories import BuurtFactory
from .factories import CBSBuurtFactory
from .factories import GasAfwc2017Factory
from .factories import Mip2016Factory
from .factories import EnergieLabelFactory

from . import authorization

log = logging.getLogger(__name__)


def pretty_data(data):
    return json.dumps(data, indent=4, sort_keys=True)


class BrowseDatasetsTestCase(APITestCase, authorization.AuthorizationSetup):
    """
    Verifies that browsing the API works correctly.
    """

    datasets = [
        'gastransitie/api/afwc',
        'gastransitie/api/buurt',
        'gastransitie/api/energielabel',
        'gastransitie/api/renovatie',
        'gastransitie/api/buurtbbox',
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
        BuurtFactory.create()
        CBSBuurtFactory.create()
        GasAfwc2017Factory.create()
        Mip2016Factory.create()
        EnergieLabelFactory.create()

    @classmethod
    def tearDownClass(cls):
        Renovatie.objects.all().delete()
        BagBuurt.objects.all().delete()
        GasAfwc2017.objects.all().delete()
        Mip2016.objects.all().delete()
        EnergieLabel.objects.all().delete()

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
            self.assertEqual(response.status_code, 401)
