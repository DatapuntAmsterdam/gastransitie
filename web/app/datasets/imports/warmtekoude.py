import os

from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import esri_json2psql
from datasets.imports.util import SRS_TO_STORE


def import_warmtekoude(datadir):
    # Stads warmte / koude net:
    pg_str = get_ogr2ogr_pgstr()
    esri_json2psql(
        os.path.join(datadir, 'warmtekoude', 'STADSWARMTEKOUDE.json'),
        pg_str,
        'gas_stadswarmtekoude_raw',
        t_srs=SRS_TO_STORE
    )
