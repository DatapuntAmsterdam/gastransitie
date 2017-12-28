#!/usr/bin/env python3
"""
This is where SQL queries that must be run after import go.
"""
from django.db import connection

FIX_AWFC2017 = """
DROP TABLE IF EXISTS new_table;
CREATE TABLE
	public.gas_afwc2017
AS (
	SELECT
		ogc_fid,
		cast(corp as varchar),
		cast(corporatie as varchar),
		cast(bouwjaar as int),
		cast(aantal_adressen as int),
		cast(aantal_corporatie as int),
		cast(percentage_corporatie as int),
		cast(gemeente as varchar),
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
