import os

import pandas
from openpyxl import load_workbook
from sqlalchemy import create_engine

from datasets.imports.util import zipped_shp2psql
from datasets.imports.util import get_sqlalchemy_db_url
from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import SRS_TO_STORE


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
    df.to_sql('gas_alliander_stoplicht_raw', engine)


def import_alliander(datadir):
    # stoplicht data
    fn = '20170829 - Stoplicht Amsterdam DISTRIBUTIELEIDINGEN (deelbaar) v0.02.xlsx'
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
