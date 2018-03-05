from django.test import TestCase

# Create your tests here.

import json
from unittest import mock
from unittest.mock import PropertyMock
from unittest.mock import MagicMock

# import models
from django.conf import settings

from datasets.models import handelsregister
from api.tests import factories

from django.core.management import call_command

FIX_DIR = settings.BASE_DIR + '/datasets'


class TestDBWriting(TestCase):
    """
    HR and SBI api code
    Test writing to database
    """

    @mock.patch('requests.get', autospec=True)
    def test_hr_sbi(self, response_mock):

        with open(FIX_DIR + '/fixtures/sbi.json') as mockjson:
            test_json = json.loads(mockjson.read())

        type(response_mock.return_value).status_code = \
            PropertyMock(return_value=200)

        type(response_mock.return_value).json = \
            MagicMock(return_value=test_json)

        call_command('run_import', '--sbicodes')
        count = handelsregister.SBIcodes.objects.count()
        self.assertEqual(count, 2)

    @mock.patch('requests.get', autospec=True)
    def test_hr_csv(self, response_mock):

        factories.BuurtFactory.create(
            naam='testbuurt',
        )

        with open(FIX_DIR + '/fixtures/ds_hr.csv') as mockcsv:
            test_csv = mockcsv.read()

        type(response_mock.return_value).status_code = \
            PropertyMock(return_value=200)

        type(response_mock.return_value).text = \
            PropertyMock(return_value=test_csv)

        call_command('run_import', '--handelsregister')
        count = handelsregister.Handelsregister.objects.count()
        self.assertEqual(count, 10)
