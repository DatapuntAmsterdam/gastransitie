#!/usr/bin/env python3
"""
This is where SQL queries that must be run after import go.
"""
from datasets.imports.util import run_sql


def reindex_bag_buurt():
    """
    Run additional SQL after restoring BAG buurt table.

    (reproject and add a spatial index)
    """
    sql = """
    ALTER TABLE "bag_buurt"
        ALTER COLUMN "geometrie"
        type Geometry(MultiPolygon, 4326)
        USING ST_Transform("geometrie", 4326);

    DROP INDEX IF EXISTS bag_buurt_idx;
    CREATE INDEX bag_buurt_idx ON public.bag_buurt USING GIST(geometrie);
    """
    run_sql(sql)
    run_sql("""VACUUM ANALYZE public.bag_buurt;""")
