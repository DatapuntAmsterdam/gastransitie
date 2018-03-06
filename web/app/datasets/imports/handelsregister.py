"""
Download per buurt alle vestigingen van dataselectie.
"""
import logging
import urllib.parse
# import argparse
import requests
from datasets.models import bag
from datasets.models.handelsregister import Handelsregister
from datasets.models.handelsregister import SBIcodes
from datasets.models.handelsregister import HandelsregisterBuurt
from datasets.models import BagBuurt

from collections import Counter

from .datapunt_auth import auth

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


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

        response.encoding = 'utf-8'
        csv = response.text
        inschrijvingen = csv.splitlines()
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


def extract_sbi_codes(inschrijvingen):
    """
    find sbi codes in hr json
    """
    sbi_counts = Counter()

    fail = 0
    seen = 0

    for h in inschrijvingen:
        if not h.data:
            fail += 1
            continue
        seen += 1

        # convert sbicodes to valid
        sbi_codes = h.data.get('SBI-code', '')
        if not sbi_codes:
            continue

        int_sbi_codes = []
        for sbi in sbi_codes.split('|'):
            # sometime there is a 'geen' value.
            sbi = sbi.strip()
            if sbi.isdigit():
                # values can be 01 != 1
                # store as string!
                int_sbi_codes.append(sbi)

        sbi_counts.update(int_sbi_codes)

    return sbi_counts


def make_rapport(inschrijvingen):
    """
    Create a summary rapport from collection of inschrijvingen at neighborhood

    - sbi information
    - sbi category information
    - sbi descriptions
    - vestigingen / inschrijvingen count
    - link to dataselectie
    """
    count = inschrijvingen.count()
    sbicount = 0

    # csb question answers tree
    q1 = Counter()
    q2 = Counter()
    q3 = Counter()

    l1 = Counter()

    sbi_description = {}

    sbi_counts = extract_sbi_codes(inschrijvingen)
    # find meta sbi information
    sbi_meta = SBIcodes.objects.filter(code__in=sbi_counts.keys())

    for sbi in sbi_meta:
        newcount = sbi_counts[sbi.code]
        sbicount += newcount
        l1key = sbi.sbi_tree.get(f'l1', [0, ''])
        l1key = l1key[1].lower()

        l1.update({l1key: newcount})

        if not sbi.qa_tree:
            # use the sbi tree.
            continue

        for i, c in enumerate([q1, q2, q3]):
            key = sbi.qa_tree.get(f'q{i+1}', '')
            if not key:
                continue
            c.update({key: newcount})

        sbi_description[sbi.code] = sbi.title

    sum_q1 = sum(q1.values())
    sum_l1 = sum(l1.values())

    if sum_q1 != sbicount:
        log.error('sum_q1 mismatch %s %s', sum_q1, sbicount)

    if sum_l1 != sbicount:
        log.error('sum_l1 mismatch %s %s', sum_l1, sbicount)

    # make rapport
    return {
        'inschrijvingen': count,
        'activiteiten': sbicount,
        'q1': q1,
        'sum_q1': sum_q1,
        'sim_l1': sum_l1,
        'l1': l1,
        # 'qa3': q3,
        # 'sbi_counts': sbi_counts,
        # 'sbi_description': sbi_description,
    }


def create_tabledata_hr_per_buurt():
    """
    For each buurt we should show some summary table
    We combine Inschrijvingen data with sbi code information
    """
    assert BagBuurt.objects.count() > 0
    assert Handelsregister.objects.count() > 0

    HandelsregisterBuurt.objects.all().delete()

    dataselectie_url = 'https://data.amsterdam.nl/#?dsd=hr&dsp=1&dsv=TABLE&dsf=buurt_naam::'   # noqa

    for buurt in BagBuurt.objects.all():
        inschrijvingen = Handelsregister.objects.filter(buurt_id=buurt.id)

        new_rapport = make_rapport(inschrijvingen)

        log.debug(
            '%s %s %s', buurt.naam,
            new_rapport['q1'].most_common(2),
            new_rapport['l1'].most_common(2)
        )

        buurt_naam = urllib.parse.quote_plus(buurt.naam)
        new_rapport['dataselectie'] = f'{dataselectie_url}{buurt_naam}'

        hb = HandelsregisterBuurt.objects.create(
            buurt_id=buurt.id,
            buurt_naam=buurt.naam,
            data=new_rapport,
        )
        hb.save()
