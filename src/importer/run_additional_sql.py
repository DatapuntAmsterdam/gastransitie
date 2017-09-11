#!/usr/bin/env python3
"""
This is where SQL queries that must be run after import go.
"""
import psycopg2

FIX_BOUWJAAR_DATATYPE = """
alter table "gas_afwc2017"
    alter column "bouwjaar" set data type int4 using "bouwjaar"::integer;
"""


def execute_sql(pg_str, sql):
    with psycopg2.connect(pg_str) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)


def get_pg_str(host, user, dbname, password):
    return 'host={} user={} dbname={} password={}'.format(
        host, user, dbname, password
    )


def main():
    print('Additional SQL run after import concludes.')
    pg_str = get_pg_str('database', 'gastransitie', 'gastransitie', 'insecure')

    execute_sql(pg_str, FIX_BOUWJAAR_DATATYPE )
    print('Done running additional SQL')


if __name__ == '__main__':
    main()
