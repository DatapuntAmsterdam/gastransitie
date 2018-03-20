import os

from datasets.imports.util import shp2psql
from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import SRS_TO_STORE
from datasets.imports.util import run_sql


_CUSTOM_SQL = """
DROP TABLE IF EXISTS public.renovaties_clean;
CREATE TABLE
    public.renovaties_clean
AS (
    SELECT
        ogc_fid,
        cast(alliantie as int),
        cast(de_key as int),
        cast(eigen_haar as int),
        cast(rochdale as int),
        cast(stadgenoot as int),
        cast(ymere as int),
        cast(eindtotaal as int),
        cast(_2017 as int) as jaar_2017,
        cast(_2018 as int) as jaar_2018,
        cast(_2019 as int) as jaar_2019,
        cast(_2020 as int) as jaar_2020,
        cast(_2021 as int) as jaar_2021,
        cast(_2022 as int) as jaar_2022,
        cast(_2023 as int) as jaar_2023,
        cast(onbekend as int) as jaar_onbekend,
        wkb_geometry
    FROM
        public.renovaties_raw
);

ALTER TABLE
    public.renovaties_clean
    ALTER COLUMN
        wkb_geometry TYPE geometry(Polygon, 4326)
    USING
        ST_Force2d(wkb_geometry);


DROP INDEX IF EXISTS renovaties_idx;
CREATE INDEX
    renovaties_idx ON public.renovaties_clean
USING GIST(wkb_geometry);
"""


def import_renovaties(datadir):
    """
    Import maps.amsterdam.nl derived map of housing corporation property.
    """

    run_sql("DROP TABLE IF EXISTS public.renovaties_raw;")

    pg_str = get_ogr2ogr_pgstr()

    shp2psql(
        os.path.join(
            datadir, 'renovaties', 'renovatiesperbuurtvanaf2017_region.shp'),
        pg_str,
        'renovaties_raw',
        t_srs=SRS_TO_STORE,
        s_srs='EPSG:28992'
    )

    run_sql(_CUSTOM_SQL)
