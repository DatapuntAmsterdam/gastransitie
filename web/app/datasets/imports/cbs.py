import os

from datasets.imports.util import zipped_shp2psql
from datasets.imports.util import get_ogr2ogr_pgstr


def import_cbs(datadir):
    """
    CBS buurt map import.
    """
    # CBS buurt kaart (2016 versie) TODO: see whether more recent is available
    pg_str = get_ogr2ogr_pgstr()
    zipped_shp2psql(
        os.path.join(datadir, 'cbs', 'buurt_2017.zip'),
        # The relevant shape files are in a subdirectory, hence the join.
        'buurt_2017.shp',
        pg_str,
        'gas_cbs_buurt_2017_raw',
        t_srs='EPSG:28992',
        nlt='PROMOTE_TO_MULTI',
        where='"gm_code"=\'GM0363\''  # only load Amsterdam
    )
