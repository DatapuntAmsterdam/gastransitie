"""
Download per buurt alle vestigingen van dataselectie.
"""
import logging
# import argparse
import requests
from datasets.models import bag
from datasets.models.handelsregister import Handelsregister
from datasets.models.handelsregister import SBIcodes

from .datapunt_auth import auth

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


# setup auth tokens!
# log.debug(auth.token_employee_plus)

headers = {'Authorization': f'Bearer {auth.token_employee_plus}'}

URL_HR = "https://acc.api.data.amsterdam.nl/dataselectie/hr/export/"
URL_SBI = "https://acc.api.data.amsterdam.nl/handelsregister/sbicodes/"

PARAMS = {
    'buurt_naam': 'AMC',
    'shape': [],
}


def get_hr_for_all_buurten():

    Handelsregister.objects.all().delete()

    for b in bag.BagBuurt.objects.all().order_by('naam'):
        PARAMS['buurt_naam'] = b.naam
        response = requests.get(URL_HR, params=PARAMS, headers=headers)

        if not response.status_code == 200:
            raise ValueError(
                f"API FAILED: {response.status_code}:{response.url}")

        csv = response.text
        inschrijvingen = csv.split('\n')[1:]

        csvheaders = inschrijvingen[0]
        data = {}
        # store every inscrhijving.
        for ves in inschrijvingen[1:]:
            data = dict(zip(csvheaders.split(';'), ves.split(';')))

            h = Handelsregister.objects.create(
                buurt_id=b.id,
                buurt_naam=b.naam,
                data=data,
            )

            h.save()

        log.debug(f'{b.naam}: {len(inschrijvingen)}')

    assert bag.BagBuurt.objects.count() > 0


def get_sbi_code_meta():
    """
    Load sbi codes from api
    """
    params = {
        'page_size': 2000,
        'detailed': True,
    }

    response = requests.get(URL_SBI, params=params, headers=headers)

    if not response.status_code == 200:
        raise ValueError(f"API SBI codes FAILED: {response.status_code}")

    json = response.json()
    SBIcodes.objects.all().delete()

    for sbi in json['results']:

        db_sbi = SBIcodes.objects.create(
            code=sbi['code'],
            title=sbi['title'],
            sbi_tree=sbi['sbi_tree'],
            qa_tree=sbi.get('qa_tree', None),
        )
        db_sbi.save()

    assert SBIcodes.objects.count() > 0
