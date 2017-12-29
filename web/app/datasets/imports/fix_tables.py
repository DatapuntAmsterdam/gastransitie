#!/usr/bin/env python3
"""
This is where SQL queries that must be run after import go.
"""
from django.db import connection

FIX_AWFC2017 = """
DROP TABLE IF EXISTS public.gas_afwc2017;
CREATE TABLE
    public.gas_afwc2017
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
        public.gas_afwc2017_raw
);
"""


def main():
    """
    Create final tables that will be used by Django.
    """
    with connection.cursor() as cursor:
        cursor.execute(FIX_AWFC2017)


if __name__ == '__main__':
    main()
