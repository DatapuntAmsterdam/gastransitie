#!/usr/bin/env python3
"""
Add (spatial) views to gas transitie database.
"""
import psycopg2

PIPELENGTH_VIEW = ""
"""
CREATE VIEW testview AS SELECT * FROM bag_buurt;
"""


def execute_sql(pg_str, sql):
    with psycopg2.connect(pg_str) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)


def main():
    print('Placeholder for addition of spatial views.')



if __name__ == '__main__':
    main()
