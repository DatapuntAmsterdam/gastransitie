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

# BUURT_MAPPING = """
# create materialized view
#         "buurtcode_mapping"
# as select
#         "bag"."vollcode" as vollcode,
#         "cbs"."bu_code" as cbscode,
#         "bag"."geometrie"
# from
#         "bag_buurt" as "bag",
#         "gas_cbs_buurt_2017" as "cbs"
# where
# case
# 	when ("cbs"."gm_code" = 'GM0363' and "cbs"."bu_naam" like "bag"."naam") then true
# 	when ST_Area(ST_Intersection("bag"."geometrie", "cbs"."wkb_geometry")) / ST_Area("bag"."geometrie") > 0.9 then true
# else false
# end
# """

#BUURT_MAPPING = """
#create materialized view
#        "buurtcode_mapping"
#as select
#        "bag"."vollcode" as vollcode,
#        "cbs"."bu_code" as cbscode,
#        "bag"."geometrie"
#from
#        "bag_buurt" as "bag",
#        "gas_cbs_buurt_2017" as "cbs"
#where
#    "cbs"."gm_code" = 'GM0363' and "cbs"."bu_naam" like "bag"."naam";
#"""

BUURTCODE_MAPPING = """
create materialized view
	buurtcode_mapping
as select
	/*count("b"."vollcode"),*/
	"b"."vollcode" as ams_code,
	"c"."bu_code" as cbs_code,
	"b"."naam" as ams_naam,
 	"c"."bu_naam" as cbs_naam,
	"b"."geometrie" as geometrie
from
	"bag_buurt" as b,
	"gas_cbs_buurt_2017" as c
where
	ST_Contains("b"."geometrie", ST_PointOnSurface("c"."wkb_geometry")) and "b"."vollcode" != 'N73g'
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
    execute_sql(pg_str, BUURTCODE_MAPPING)
    print('Test view created')


if __name__ == '__main__':
    main()
