import os

from datasets.imports.util import esri_json2psql
from datasets.imports.util import get_ogr2ogr_pgstr


def import_corporatie_bezit(datadir):
    """
    Import maps.amsterdam.nl derived map of housing corporation property.
    """
    pg_str = get_ogr2ogr_pgstr()
    esri_json2psql(
        os.path.join(datadir, 'corporatie_bezit', 'AFWC_2017.json'),
        pg_str,
        'gas_afwc2017_raw',
        t_srs='EPSG:28992'
    )
