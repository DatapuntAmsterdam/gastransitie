import os
import logging

import pandas
from openpyxl import load_workbook
from sqlalchemy import create_engine
from django.db import connections
from datasets.models import bag
from datasets.models import alliander

from datasets.imports.util import zipped_shp2psql
from datasets.imports.util import get_sqlalchemy_db_url
from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import SRS_TO_STORE


log = logging.getLogger(__name__)


def _load_stoplicht_alliander(filename):
    """
    Load the initial Alliander stoplicht data set.
    """
    # Excel wrangling:
    sheetname = "Buurten Stoplicht Liander"
    worksheet = load_workbook(filename=filename)[sheetname]
    columns = [x.value for x in worksheet[1]]
    data = ([x.value for x in row] for row in worksheet.iter_rows(min_row=2))

    df = pandas.DataFrame(data, columns=columns)

    # Write our data to database
    engine = create_engine(get_sqlalchemy_db_url())
    df.to_sql('gas_alliander_stoplicht_raw', engine, if_exists='replace')


def load_xslx_verbruik_kv(datadir):
    """
    Verbruik P6 data. (klein)
    """
    # LianderKV01012018.xlsx
    xls_path = os.path.join(datadir, 'alliander', 'LianderKV01012018.xlsx')
    log.debug('Loading worksheet')
    sheetname = "Export Worksheet"
    wb = load_workbook(filename=xls_path, read_only=True)
    worksheet = wb[sheetname]
    worksheet.max_row = worksheet.max_column = None
    columns = [x.value for x in worksheet[1]]
    # replace invalid sql chars
    columns = [x.replace('%', '') for x in columns]
    columns = [x.replace('(', ' ') for x in columns]
    columns = [x.replace(')', ' ') for x in columns]

    log.debug('Columns data %s', columns)
    log.debug('Loading data')

    data = []

    for ri, row in enumerate(worksheet.iter_rows(min_row=2)):
        if ri % 5000 == 0:
            log.debug('rows..%d', ri)

        if row[6].value != 'AMSTERDAM':
            continue

        data.append([x.value for x in row])

    log.debug('Create pandas df data')
    df = pandas.DataFrame(data, columns=columns)
    engine = create_engine(get_sqlalchemy_db_url())
    log.debug('dump to sql')
    df.to_sql('alliander_kv', engine, if_exists='replace')


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def create_p6_buurt():
    sql = f"""
    SELECT DISTINCT postcode, b.id as id, b.vollcode as code, b.naam as naam
    FROM bag_nummeraanduiding n, bag_verblijfsobject v, bag_buurt b
    WHERE n.verblijfsobject_id = v.id
    AND v.buurt_id = b.id
    AND postcode is not null
    AND postcode != ''
    ORDER BY naam
    """

    with connections['bag'].cursor() as cursor:
        cursor.execute(sql)
        data = dictfetchall(cursor)

    postcode_buurt = {}

    for item in data:
        postcode_buurt[item['postcode']] = {
                'naam': item['naam'],
                'id': item['id'],
                'vollcode': item['code'],
                }

    return postcode_buurt


def make_empty_rapports():
    """Create empty energy rapports for each buurt
    """
    buurten = {}

    # make empty rapports.
    for b in bag.BagBuurt.objects.using('bag').all().order_by('naam'):
        buurt_rapport = {
            'naam': b.naam,
            'id': b.id,
            'vollcode': b.vollcode,
            'gas': {
                'aansluitingen': 0,
                'm3': 0,
                'leveringsrichting': []
            },
            'elk': {
                'aansluitingen': 0,
                'Kwh': 0,
                'leveringsrichting': []
            }
        }
        buurten[b.id] = buurt_rapport

    return buurten


def verbruik_per_buurt(p6_buurt):
    """Stel gasverbruik per buurt vast.
    """
    alliander.VerbruikPerBuurt.objects.all().delete()
    b_rapports = make_empty_rapports()

    for p6data in alliander.AllianderKv.objects.all().order_by('postcode_van'):
        buurt = p6_buurt.get(p6data.postcode_van)
        if not buurt:
            log.debug('skipped %s', p6data.postcode_van)
            continue

        br = b_rapports[buurt['id']]

        if p6data.productsoort == 'GAS':
            br['gas']['aansluitingen'] += p6data.aantal_aansluitingen
            br['gas']['m3'] += p6data.sjv
            br['gas']['leveringsrichting'].append(p6data.leveringsrichting)
        else:
            br['elk']['aansluitingen'] += p6data.aantal_aansluitingen
            br['elk']['Kwh'] += p6data.sjv
            br['elk']['leveringsrichting'].append(p6data.leveringsrichting)

        avb = alliander.VerbruikPerBuurt(
            id=br['id'],
            vollcode=br['vollcode'],
            naam=br['naam'],
            data=br,
        )
        avb.save()


def import_alliander(datadir):
    """Import alliander data.

    -leidingen
    -verbruik
    """
    load_xslx_verbruik_kv(datadir)
    p6_buurt = create_p6_buurt()
    verbruik_per_buurt(p6_buurt)

    # stoplicht data
    # fn = '20170829 - Stoplicht Amsterdam DISTRIBUTIELEIDINGEN (deelbaar) v0.02.xlsx'  # noqa
    # _load_stoplicht_alliander(os.path.join(datadir, 'alliander', fn))

    # Alliander data for gas mains
    pg_str = get_ogr2ogr_pgstr()

    zipped_shp2psql(
        os.path.join(datadir, 'alliander', 'Groen_Amsterdam.zip'),
        'Groen_Amsterdam.shp',
        pg_str,
        'gas_alliander_gas_groen_raw',
        t_srs=SRS_TO_STORE,
        nlt='PROMOTE_TO_MULTI',
        s_srs='EPSG:28992'
    )

    zipped_shp2psql(
        os.path.join(datadir, 'alliander', 'Oranje_Amsterdam.zip'),
        'Oranje_Amsterdam.shp',
        pg_str,
        'gas_alliander_gas_oranje_raw',
        t_srs=SRS_TO_STORE,
        s_srs='EPSG:28992'
    )
