"""
Download per BRK / BAG informatie per buurt / per coorporatie.

We use the BAG API, and SQL for the more compliated data.

"""

import logging
import time
# import urllib.parse
# import argparse
import requests
from datasets.models import bag

# from collections import Counter

from .datapunt_auth import auth

from django.db import connections

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

STATUS_LINE = '%4s %20s %6d'
STATUS_LINE_C = '%4s %20s %6d %-20s'

# ROOT = "http://127.0.0.1:8081"
ROOT = "https://acc.api.data.amsterdam.nl"

# headers = {'Authorization': f'Bearer {auth.token_employee_plus}'}
headers = auth.GetAccessToken().get_auth_header()


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

    start = time.time()
    response = requests.get(url, params=params, headers=headers)

    if not response.status_code == 200:
        raise ValueError(
            f"API FAILED: {response.status_code}:{response.url}")

    delta = time.time() - start
    if delta > 6:
        log.error('SLOW %.2f %s %s', delta, url, params)
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
            'aard_zakelijk_recht': 2  # eigenaars rechten
        }

        c_json = get_json(URL_RECHT, params)
        c_count = c_json['count']

        if c_count:
            log.debug(
                STATUS_LINE_C,
                buurt.vollcode, 'C', c_count, c_naam)

        if not c_count:
            continue

        corportatie_rapport[c_naam] = c_count

    return corportatie_rapport


def make_bezit_rapport(buurt):
    """Corporatie vbo's sql

    Achterhaal groote bezitters in de buurt
    """

    sql = f"""
SELECT
   s.statutaire_naam, s.naam, count(*) as thecounts
FROM
     bag_verblijfsobject v,
     brk_zakelijkrechtverblijfsobjectrelatie zr,
     brk_zakelijkrecht r,
     brk_kadastraalsubject s
WHERE
    r.kadastraal_subject_id = s.id
AND zr.zakelijk_recht_id = r.id
AND v.id = zr.verblijfsobject_id
AND v.buurt_id = '{buurt.id}'
GROUP BY (s.statutaire_naam, s.naam) order by thecounts desc
    """

    with connections['bag'].cursor() as cursor:
        cursor.execute(sql)
        data = dictfetchall(cursor)

    big_owners = []

    for item in data:
        if item['thecounts'] > 5:
            big_owners.append(item)

    return big_owners


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def bewoners_per_buurt(buurt) -> int:
    """Stel de bewoners per buurt vast.

    Bewoners hebben eigendoms recht op hun woonadres.
    """

    sql = f"""
SELECT count(distinct(v.id))
FROM brk_kadastraalsubject s,
     brk_zakelijkrechtverblijfsobjectrelatie zr,
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
AND v."buurt_id" = '{buurt.id}'
    """

    with connections['bag'].cursor() as cursor:
        cursor.execute(sql)
        data = dictfetchall(cursor)
        log.debug('Bewoners %s: %s', data[0]['count'], buurt.naam)
        return data[0]['count']


def gebruik_per_buurt(buurt) -> dict:
    """Gebruik van verblijfsobjecten in de buurt.
    """

    sql = f"""
        SELECT count(v.id), g.omschrijving, g.code
        FROM bag_verblijfsobject v , bag_gebruik g
        WHERE v.gebruik_id = g.code
        AND v."buurt_id" = '{buurt.id}'
        GROUP BY (g.omschrijving, g.code)
    """

    with connections['bag'].cursor() as cursor:
        cursor.execute(sql)
        data = dictfetchall(cursor)
        # log.debug('Gebruik %s: %s', data, buurt.naam)
        return data


def get_bouwkundige_verdeling(buurt) -> dict:
    """Bouwkundige samenstelling

    Deze cijfers staan ook in BBGA.
    """

    ranges = [
        (0, 40),
        (40, 50),
        (50, 60),
        (60, 70),
        (70, 80),
        (80, 90),
        (90, 120),
        (120, 180),
        (180, 300),
        (300, 400),
        (400, 1000),
        (1000, 2000),
        (2000, 3000),
        (3000, 5000),
        (5000, 999999),
    ]

    groote_verdeling = {}

    for _min, _max in ranges:

        sql = f"""
            SELECT count(v.id)
            FROM bag_verblijfsobject v
            WHERE v."buurt_id" = '{buurt.id}'
            AND v.oppervlakte > {_min}
            AND v.oppervlakte <= {_max}
        """
        with connections['bag'].cursor() as cursor:
            cursor.execute(sql)
            data = dictfetchall(cursor)
            groote_verdeling[f'{_min}-{_max}'] = data[0]['count']

    assert len(ranges) == len(groote_verdeling)
    log.debug('Grootte: %s', groote_verdeling)
    return groote_verdeling


def get_bouwjaar_verdeling(buurt) -> dict:
    """Bouwjaar verdeling in buurt.
    """

    ranges = [
        (-10000, 1850),
        (1850, 1900),
        (1900, 1920),
        (1920, 1930),
        (1930, 1940),
        (1940, 1950),
        (1950, 1960),
        (1960, 1970),
        (1970, 1980),
        (1980, 1990),
        (1990, 2000),
        (2000, 2010),
        (2010, 2020),
        (2020, 2030),
    ]

    bouwjaar_verdeling = {}

    for _min, _max in ranges:
        sql = f"""
            SELECT count(v.id)
            FROM bag_verblijfsobject v,
                 bag_pand p,
                 bag_verblijfsobjectpandrelatie vp
            WHERE v."buurt_id" = '{buurt.id}'
            AND p.id = vp."pand_id"
            AND v.id = vp."verblijfsobject_id"
            AND p.bouwjaar > {_min}
            AND p.bouwjaar <= {_max}
        """  # noqa
        with connections['bag'].cursor() as cursor:
            cursor.execute(sql)
            data = dictfetchall(cursor)
            bouwjaar_verdeling[f'{_min}-{_max}'] = data[0]['count']

    assert len(ranges) == len(bouwjaar_verdeling)
    log.debug('Bouwjaren: %s', bouwjaar_verdeling)
    return bouwjaar_verdeling


def get_bag_brk_for_all_buurten():
    """
    - totaal VBO
    - VBO's per corporaties
    - eigenaar / verhuur
    - geometrie per vbo
    - bouwblok/geo van vbo's?
    """
    bag.BagRapport.objects.all().delete()

    for b in bag.BagBuurt.objects.using('bag').all().order_by('naam'):  # .filter(vollcode='M57a'):
        # bewoners
        bewoner_count = bewoners_per_buurt(b)
        bag_gebruik = gebruik_per_buurt(b)
        bouwkundige_groote = get_bouwkundige_verdeling(b)
        bouwjaar_verdeling = get_bouwjaar_verdeling(b)

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
        # c_rapport = make_corporatie_rapport(b)
        # print(c_rapport)
        bezit_rapport = make_bezit_rapport(b)

        buurt_rapport = {
            'vbo_count': vbo_count,
            'subjecten_count': sub_count,
            'natuurlijke_subjecten': n_sub_count,
            'niet_natuurlijke_subjecten': nn_sub_count,
            'groot_bezitters': bezit_rapport,
            'bewoners_count': bewoner_count,
            'gebruik': bag_gebruik,
            'bouwkundige_groote': bouwkundige_groote,
            'bouwjaar_verdeling': bouwjaar_verdeling,
        }

        # Create Buurt BAG / corporatie rapport
        r = bag.BagRapport(
            id=b.id,
            code=b.code,
            vollcode=b.vollcode,
            naam=b.naam,
            data=buurt_rapport,
        )

        r.save()
