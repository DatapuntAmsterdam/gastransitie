"""
Utility functions that deal with ogr2ogr and postgresql.
"""
import os
import tempfile
import subprocess
import logging

from sqlalchemy.engine.url import URL
from django.conf import settings
from django.db import connection

SRS_TO_STORE = 'EPSG:4326'


def get_sqlalchemy_db_url():
    """
    Pandas to_sql needs SQLAlchemy, but we want Django's settings, hence:
    """
    db = settings.DATABASES['default']
    engines_mapping = {
        'django.contrib.gis.db.backends.postgis': 'postgresql',
        'django.db.backends.sqlite3': 'sqlite',
    }

    return URL(
        drivername=engines_mapping[db['ENGINE']],
        username=db['USER'],
        host=db['HOST'],
        port=db['PORT'],
        database=db['NAME'],
        password=db['PASSWORD'],
    )


def get_ogr2ogr_pgstr():
    """
    Connection string for ogr2ogr from Django's database settings.
    """
    db = settings.DATABASES['default']

    return 'PG:host={} port={} user={} dbname={} password={}'.format(
        db['HOST'],
        db['PORT'],
        db['USER'],
        db['NAME'],
        db['PASSWORD'],
    )


class NonZeroReturnCode(Exception):
    pass


def scrub(l):
    out = []
    for x in l:
        if x.strip().startswith('PG:'):
            out.append('PG: <CONNECTION STRING REDACTED>')
        else:
            out.append(x)
    return out


def run_command_sync(cmd, allow_fail=False):
    logging.debug('Running %s', scrub(cmd))
#    logging.debug('Running %s', cmd)
    p = subprocess.Popen(cmd)
    p.wait()

    if p.returncode != 0 and not allow_fail:
        raise NonZeroReturnCode

    return p.returncode


def shp2psql(shp_filename, pg_str, layer_name, **kwargs):
    cmd = [
        'ogr2ogr', '-nln', layer_name, '-F', 'PostgreSQL',
        '-overwrite', '--config', 'PG_USE_COPY', 'YES',
    ]
    if 't_srs' in kwargs:
        cmd.extend(['-t_srs', kwargs['t_srs']])
    if 's_srs' in kwargs:
        cmd.extend(['-s_srs', kwargs['s_srs']])
    if 'nlt' in kwargs:
        cmd.extend(['-nlt', kwargs['nlt']])
    if 'where' in kwargs:
        cmd.extend(['-where', kwargs['where']])
    cmd.extend([pg_str, shp_filename])
    run_command_sync(cmd)


def zipped_shp2psql(zip_filename, shp_filename, pg_str, layer_name, **kwargs):
    with tempfile.TemporaryDirectory() as tempdir:
        cmd = ['unzip', '-d', tempdir, zip_filename]
        run_command_sync(cmd)

        shp2psql(
            os.path.join(tempdir, shp_filename), pg_str, layer_name, **kwargs)


def tab2psql(tab_filename, pg_str, layer_name, **kwargs):
    with tempfile.TemporaryDirectory() as tempdir:
        shp_filename = os.path.join(tempdir, tab_filename[:-4] + '.shp')

        # Convert from Mapinfo file format to shapefile:
        cmd = ['ogr2ogr', '-F',
               '-overwrite',
               '-lco', 'ENCODING', 'UTF-8',
               'ESRI Shapefile', shp_filename, tab_filename]

        run_command_sync(cmd)

        # Import shapefile into PostgreSQL:
        cmd = [
            'ogr2ogr',
            '-nln', layer_name,
            '-F', 'PostgreSQL',
            pg_str,
            '-overwrite', '--config', 'PG_USE_COPY', 'YES',
            shp_filename
        ]
        run_command_sync(cmd)


def esri_json2psql(json_filename, pg_str, layer_name, **kwargs):
    # first attempt:
    # https://gis.stackexchange.com/questions/13029/converting-arcgis-server-json-to-geojson
    cmd = ['ogr2ogr', '-nln', layer_name, '-F', 'PostgreSQL',
           '-overwrite',
           '--config', 'PG_USE_COPY', 'YES']
    if 't_srs' in kwargs:
        cmd.extend(['-t_srs', kwargs['t_srs']])
    else:
        cmd.extend(['-t_srs', 'EPSG:28992'])
    cmd.extend([pg_str, json_filename])
    run_command_sync(cmd)


def run_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
