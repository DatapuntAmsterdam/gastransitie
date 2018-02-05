import os

from datasets.imports.util import esri_json2psql
from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import SRS_TO_STORE
from datasets.imports.util import run_sql


_CUSTOM_SQL = """
DROP TABLE IF EXISTS public.mip2016_clean;
CREATE TABLE
    public.mip2016_clean
AS (
    SELECT
        ogc_fid,
        cast(gsu as varchar(255)) as datum,
        cast(organisatie as varchar(255)) as organisatie,
        cast(ambtelijk_opdrachtgever as varchar(255)) as opdrachtgever,
        cast(mip_nummer as varchar(255)) as nummer,
        cast(projectnaam as varchar(255)) as omschrijving,
        wkb_geometry
    FROM
        public.mip2016_raw
);
DROP INDEX IF EXISTS mip2016_idx;
CREATE INDEX mip2016_idx ON public.mip2016_clean USING GIST(wkb_geometry);
"""
# Note skipping all boolean fields like noord in the raw data.


def import_mip(datadir):
    """
    Import multi year investment plan 2016.
    """

    pg_str = get_ogr2ogr_pgstr()
    esri_json2psql(
        os.path.join(datadir, 'mip', 'MIP2016.json'),
        pg_str,
        'mip2016_raw',
        t_srs=SRS_TO_STORE
    )


def fix_tables():
    run_sql(_CUSTOM_SQL)
    run_sql("""VACUUM ANALYZE public.mip2016_clean;""")
