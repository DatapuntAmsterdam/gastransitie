import os

from datasets.imports.util import esri_json2psql
from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import SRS_TO_STORE
from datasets.imports.util import run_sql

_CUSTOM_SQL = """
DROP TABLE IF EXISTS public.afwc2017_clean;
CREATE TABLE
    public.afwc2017_clean
AS (
    SELECT
        ogc_fid,
        cast(corp as varchar(255)),
        cast(corporatie as varchar(255)),
        cast(bouwjaar as int),
        cast(aantal_adressen as int),
        cast(aantal_corporatie as int),
        cast(percentage_corporatie as int),
        cast(gemeente as varchar(255)),
        cast(perc as int),
        wkb_geometry
    FROM
        public.afwc2017_raw
);

DROP INDEX IF EXISTS afwc2017_idx;
CREATE INDEX afwc2017_idx ON public.afwc2017_clean USING GIST(wkb_geometry);
"""


def import_corporatie_bezit(datadir):
    """
    Import maps.amsterdam.nl derived map of housing corporation property.
    """
    pg_str = get_ogr2ogr_pgstr()
    esri_json2psql(
        os.path.join(datadir, 'corporatie_bezit', 'AFWC_2017.json'),
        pg_str,
        'afwc2017_raw',
        t_srs=SRS_TO_STORE
    )


def fix_tables():
    run_sql(_CUSTOM_SQL)
    run_sql("""VACUUM ANALYZE public.afwc2017_clean;""")
