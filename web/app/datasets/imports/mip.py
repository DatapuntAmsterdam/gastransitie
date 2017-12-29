import os

from datasets.imports.util import esri_json2psql
from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import SRS_TO_STORE


def import_mip(datadir):
    """
    Import multi year investment plan 2016.
    """

    pg_str = get_ogr2ogr_pgstr()
    esri_json2psql(
        os.path.join(datadir, 'mip', 'MIP2016.json'),
        pg_str,
        'gas_mip2016_raw',
        t_srs=SRS_TO_STORE
    )
