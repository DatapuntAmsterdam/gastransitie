#!/usr/bin/env python3
"""
Add (spatial) views to gas transitie database.
"""
import psycopg2

GAS_GROEN_PER_BUURT = """
create view
  gas_groen_per_buurt
as select
  b.vollcode,
  sum(ST_Length(g.wkb_geometry))/1000 as lengte,
  b.geometrie
from
  bag_buurt as b,
  gas_alliander_gas_groen as g
where
  ST_Contains(b.geometrie, g.wkb_geometry)
group by
  b.vollcode,
  b.geometrie
order by
  lengte desc;
"""

GAS_ORANJE_PER_BUURT = """
create view
  gas_oranje_per_buurt
as select
  b.vollcode,
  sum(ST_Length(g.wkb_geometry))/1000 as lengte,
  b.geometrie
from
  bag_buurt as b,
  gas_alliander_gas_oranje as g
where
  ST_Contains(b.geometrie, g.wkb_geometry)
group by
  b.vollcode,
  b.geometrie
order by
  lengte desc;
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
    print('Placeholder for addition of spatial views.')
    pg_str = get_pg_str('database', 'gastransitie', 'gastransitie', 'insecure')

    execute_sql(pg_str, GAS_GROEN_PER_BUURT)
    execute_sql(pg_str, GAS_ORANJE_PER_BUURT)
    print('Test view created')


if __name__ == '__main__':
    main()
