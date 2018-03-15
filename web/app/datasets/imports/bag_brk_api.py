"""
Download per BRK / BAG informatie per buurt / per coorporatie.
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

STATUS_LINE = '%4s %20s %6d'
STATUS_LINE_C = '%4s %20s %6d %-20s'

ROOT = "http://127.0.0.1:8000"

headers = {'Authorization': f'Bearer {auth.token_employee_plus}'}

URL_VBO = f"{ROOT}/bag/verblijfsobject/"
URL_SUB = f"{ROOT}/brk/subject/"
URL_RECHT = f"{ROOT}/brk/zakelijk-recht/"
# URL_ = "https://acc.api.data.amsterdam.nl/handelsregister/sbicodes/"

PARAMS = {
    'buurt_naam': 'AMC',
}


WONING_CORPORATIES = [
    ("NL.KAD.Persoon.519506319", "Stadgenoot Ontwikkeling II BV"),
    ("NL.KAD.Persoon.122620316", "Stichting DUWO"),
    ("NL.KAD.Persoon.172013385", "Stichting Stadgenoot"),
    ("NL.KAD.Persoon.402718637", "Stichting Ymere"),
    ("NL.KAD.Persoon.199400597", "Woonstichting Lieven de Key"),
    ("NL.KAD.Persoon.122930769", "Woningstichting Eigen Haard"),
    ("NL.KAD.Persoon.406261333", "Stadsherstel II N.V."),   # noqa
    ("NL.KAD.Persoon.172090014", "Stadsherstel Ii N.V."),   # noqa
    ("NL.KAD.Persoon.172013404", "Stichting de Alliantie"),
    ("NL.KAD.Persoon.11731803",  "Stichting Woonzorg Nederland"),
    ("NL.KAD.Persoon.202352911", "Woningstichting Rochdale"),
    ("NL.KAD.Persoon.172206338", "Projectontwikkeling Ymere B.V."),
    ("NL.KAD.Persoon.172211115", "Ymere II B.V."),  # noqa
    ("NL.KAD.Persoon.198921986", "Ymere Ontwikkeling B.V."),
    ("NL.KAD.Persoon.459362889", "Stadsherstel Amsterdam N.V."),
    ("NL.KAD.Persoon.172013435", "Amsterdamsche Cooperatieve Woningvereeniging"),  # noqa
    ("NL.KAD.Persoon.333687163", "Ymere VI B.V."),  # noqa
    ("NL.KAD.Persoon.252140640", "Monumenten De Key B.V."),
    ("NL.KAD.Persoon.11734470",  "Stichting Habion"),
    ("NL.KAD.Persoon.462322843", "Stichting Kantoorgebouwen Eigen Haard"),
    ("NL.KAD.Persoon.326155554", "Rochdale Participaties B.V."),
    ("NL.KAD.Persoon.308371616", "eigen haard projectontwikkeling b.v."),
    ("NL.KAD.Persoon.172013595", "Stichting Ymere"),
    ("NL.KAD.Persoon.184029003", "Volkshuisvestingsgroep Wooncompagnie"),
    ("NL.KAD.Persoon.197114580", "Ymere VIII B.V."),
    ("NL.KAD.Persoon.172107996", "De Goede Woning"),
    ("NL.KAD.Persoon.422423013", "Stichting De Alliantie"),
    ("NL.KAD.Persoon.122912658", "Stichting Eigen Haard Assendelft"),
    ("NL.KAD.Persoon.197352789", "Stichting Wooncompagnie"),
    ("NL.KAD.Persoon.478316430", "Ymere XII B.V."),
    ("NL.KAD.Persoon.503138989", "Stadgenoot Ontwikkeling I B.V."),
    ("NL.KAD.Persoon.499112361", "Stadgenoot Vastgoed B.V.,"),
    ("NL.KAD.Persoon.172219833", "Stichting Wooncompagnie"),
]


def get_json(url, params):

    response = requests.get(url, params=params, headers=headers)

    if not response.status_code == 200:
        raise ValueError(
            f"API FAILED: {response.status_code}:{response.url}")

    return response.json()

"""
?verblijfsobjecten__landelijk_id=&verblijfsobjecten__id=
&verblijfsobjecten__buurt=03630000000798
&verblijfsobject=&aard_zakelijk_recht
=2&kadastraal_object=&kadastraal_subject=NL.KAD.Persoon.497464431&kadastraal_subject__type=1
"""


def make_corporatie_rapport(buurt):
    corportatie_rapport = {}

    for c_persoon, c_naam in WONING_CORPORATIES:
        params = {
            'verblijfsobjecten__buurt': buurt.id,
            'kadastraal_subject': c_persoon,
            'aard_zakelijk_recht': 2 # eigenaars rechten
        }

        c_json = get_json(URL_RECHT, params)
        c_count = c_json['count']

        log.debug(
            STATUS_LINE_C,
            buurt.vollcode, 'C', c_count, c_naam)

        if not c_count:
            continue

        corportatie_rapport['c_naam'] = c_count

    return corportatie_rapport


def bewoners_per_buurt():
    """
    Stel de bewoners per buurt vast.
    ze hebben eigendoms recht op hun adres.
    """
    sql = """
SELECT count(distinct(v.id))  /*, s.id, s.naam, a.openbareruimte_naam, a.huisnummer, a.toevoeging */  # noqa
FROM brk_kadastraalsubject s,
     brk_zakelijkrechtverblijfsobjectrelatie zr ,
     brk_zakelijkrecht r,
     bag_verblijfsobject v,
     brk_adres a
WHERE
    r.kadastraal_subject_id = s.id
AND r.aard_zakelijk_recht_id = '2'
AND zr.zakelijk_recht_id = r.id
AND v.id = zr.verblijfsobject_id
AND a.id = s.woonadres_id
AND v."_openbare_ruimte_naam" = a.openbareruimte_naam
AND v."_huisnummer" = a.huisnummer
AND v."_huisletter" = a.huisletter
AND v."_huisnummer_toevoeging" = a.toevoeging
    """


def get_bag_brk_for_all_buurten():
    """
    - totaal VBO
    - VBO's per corporaties
    - eigenaar / verhuur
    - geometrie per vbo
    - bouwblok/geo van vbo's?
    """

    buurt_rapport = {}

    for b in bag.BagBuurt.objects.all().order_by('naam')[:3]:
        # Totaal VBO's
        parameters = {'buurt': b.id}
        vbo_json = get_json(URL_VBO, parameters)
        vbo_count = vbo_json['count']
        log.debug(STATUS_LINE, b.vollcode, 'VBO', vbo_count)

        # Totaal eigenaars
        parameters = {'buurt': b.vollcode, 'zakelijk_recht': 2}
        sub_json = get_json(URL_SUB, parameters)
        sub_count = sub_json['count']
        log.debug(STATUS_LINE, b.vollcode, 'EIGENAARS', sub_count)

        # Natuurlijk
        parameters = {'buurt': b.vollcode, 'type': 0, 'zakelijk_recht': 2}
        sub_json = get_json(URL_SUB, parameters)
        n_sub_count = sub_json['count']
        log.debug(STATUS_LINE, b.vollcode, 'SUBJECTEN NATUURLIJK', n_sub_count)

        # Niet Natuurlijk
        parameters = {'buurt': b.vollcode, 'type': 1, 'zakelijk_recht': 2}
        sub_json = get_json(URL_SUB, parameters)
        nn_sub_count = sub_json['count']
        log.debug(STATUS_LINE, b.vollcode, 'SUBJECTEN NIET N', nn_sub_count)

        # Corporatie bezit
        make_corporatie_rapport(b)
