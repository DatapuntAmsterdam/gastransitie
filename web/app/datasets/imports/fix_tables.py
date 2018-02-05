#!/usr/bin/env python3
"""
This is where SQL queries that must be run after import go.
"""
from datasets.imports import corporatie_bezit
from datasets.imports import cbs
from datasets.imports import mip
from datasets.imports import energie_labels
from datasets.imports.util import run_sql


def fix_bag_buurt():
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


def main():
    """
    Create final tables that will be used by Django.
    """
    corporatie_bezit.fix_tables()
    cbs.fix_tables()
    mip.fix_tables()
    energie_labels.fix_tables()
    fix_bag_buurt()


if __name__ == '__main__':
    main()
