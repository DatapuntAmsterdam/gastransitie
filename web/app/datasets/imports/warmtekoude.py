import os

from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import esri_json2psql
from datasets.imports.util import SRS_TO_STORE
from datasets.imports.util import run_sql


_CUSTOM_SQL = """
DROP TABLE IF EXISTS public.warmtekoude_clean;
CREATE TABLE
    public.warmtekoude_clean
AS (
    SELECT
        ogc_fid,
        cast(type_net as varchar(255)),
        cast(eigenaar_net as varchar(255)),
        cast(soort_leiding as varchar(255)),
        cast(status as varchar(255)),
        cast(selectie as varchar(255)),
        cast(filter as varchar(255)),
        wkb_geometry
    FROM
        public.warmtekoude_raw
);

DROP INDEX IF EXISTS warmtekoude_idx;
CREATE INDEX warmtekoude_idx ON public.warmtekoude_clean USING GIST(wkb_geometry);
"""


def import_warmtekoude(datadir):
    # Stads warmte / koude net:
    pg_str = get_ogr2ogr_pgstr()
    esri_json2psql(
        os.path.join(datadir, 'warmtekoude', 'STADSWARMTEKOUDE.json'),
        pg_str,
        'warmtekoude_raw',
        t_srs=SRS_TO_STORE
    )


def fix_tables():
    run_sql(_CUSTOM_SQL)
    run_sql("""VACUUM ANALYZE public.warmtekoude_clean;""")
