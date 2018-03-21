import os


from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import esri_json2psql
from datasets.imports.util import SRS_TO_STORE
from datasets.imports.util import run_sql

_CUSTOM_SQL = """
DROP TABLE IF EXISTS public.energie_labels_clean;
CREATE TABLE
    public.energie_labels_clean
AS (
    SELECT
        ogc_fid,
        cast(energielabel as varchar(1)),
        wkb_geometry
    FROM public.energie_labels_raw
);
DROP INDEX IF EXISTS energie_labels_idx;
CREATE INDEX
    energie_labels_idx ON public.energie_labels_clean
USING GIST(wkb_geometry);
"""


def import_energie_labels(datadir):
    # energie labels (van maps.amsterdam.nl open geodata)
    pg_str = get_ogr2ogr_pgstr()
    esri_json2psql(
        os.path.join(datadir, 'energie_labels', 'ENERGIE_LABELS.json'),
        pg_str,
        'energie_labels_raw',
        t_srs=SRS_TO_STORE
    )

    run_sql(_CUSTOM_SQL)
