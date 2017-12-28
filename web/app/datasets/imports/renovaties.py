import os

from datasets.imports.util import shp2psql
from datasets.imports.util import get_ogr2ogr_pgstr


def import_renovaties(datadir):
    """
    Import maps.amsterdam.nl derived map of housing corporation property.
    """
    pg_str = get_ogr2ogr_pgstr()

    shp2psql(
        os.path.join(
            datadir, 'renovaties', 'renovatiesperbuurtvanaf2017_region.shp'),
        pg_str,
        'gas_woningbouw_renovatie_plannen_raw',
        t_srs='EPSG:28992'
    )
