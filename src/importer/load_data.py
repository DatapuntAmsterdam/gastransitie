import os
import tempfile
import subprocess
import logging
import argparse


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


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


def get_pg_str(host, user, dbname, password):
    return 'PG:host={} user={} dbname={} password={}'.format(
        host, user, dbname, password
    )


def shp2psql(shp_filename, pg_str, layer_name, **kwargs):
    cmd = ['ogr2ogr', '-nln', layer_name, '-F', 'PostgreSQL']
    if 't_srs' in kwargs:
        cmd.extend(['-t_srs', kwargs['t_srs']])
    cmd.extend([pg_str, shp_filename])
    run_command_sync(cmd)


def zipped_shp2psql(zip_filename, shp_filename, pg_str, layer_name, **kwargs):
    # Assume for now no structure in zip file, hence shp_filename has no
    # directory in it.
    shp_filename = os.path.split(shp_filename)[1]  # enforce assumption
    with tempfile.TemporaryDirectory() as tempdir:
        cmd = ['unzip', '-d', tempdir, zip_filename]
        run_command_sync(cmd)

        shp2psql(os.path.join(tempdir, shp_filename), pg_str, layer_name, **kwargs)


def tab2psql(tab_filename, pg_str, layer_name, **kwargs):
    with tempfile.TemporaryDirectory() as tempdir:
        shp_filename = os.path.join(tempdir, tab_filename[:-4] + '.shp')

        # Convert from Mapinfo file format to shapefile:
        cmd = ['ogr2ogr', '-F', 'ESRI Shapefile', shp_filename, tab_filename]
        run_command_sync(cmd)

        # Import shapefile into PostgreSQL:
        cmd = ['ogr2ogr', '-nln', layer_name, '-F', 'PostgreSQL', pg_str, shp_filename]
        run_command_sync(cmd)


def esri_json2psql(json_filename, pg_str, layer_name, **kwargs):
    # first attempt:
    # https://gis.stackexchange.com/questions/13029/converting-arcgis-server-json-to-geojson
    cmd = ['ogr2ogr', '-t_srs', 'EPSG:28992', '-nln', layer_name, '-F', 'PostgreSQL', pg_str, json_filename]
    run_command_sync(cmd)


def main(datadir):
    # Current setup is to run locally, using datapunt Postgres image and the
    # builder image.
    pg_str = get_pg_str('database', 'gastransitie', 'gastransitie', 'insecure')

    # renovatieplannen
    shp2psql(
        os.path.join(datadir, 'renovaties', 'renovatiesperbuurtvanaf2017_region.shp'),
        pg_str,
        'gas_woningbouw_renovatie_plannen'
    )

    # alliander data
    zipped_shp2psql(
        os.path.join(datadir, 'alliander', 'Groen_Amsterdam.zip'),
        'Groen_Amsterdam.shp',
        pg_str,
        'gas_alliander_gas_groen',
        t_srs='EPSG:28992'
    )

    zipped_shp2psql(
        os.path.join(datadir, 'alliander', 'Oranje_Amsterdam.zip'),
        'Oranje_Amsterdam.shp',
        pg_str,
        'gas_alliander_gas_oranje',
        t_srs='EPSG:28992'
    )

    # Stads warmte / koude net:
    esri_json2psql(
        os.path.join(datadir, 'warmtekoude', 'STADSWARMTEKOUDE.json'),
        pg_str,
        'gas_stadswarmtekoude'
    )

    # MIP2016
    esri_json2psql(
        os.path.join(datadir, 'mip', 'MIP2016.json'),
        pg_str,
        'gas_mip2016'
    )

    # corporatie bezit 2017
    esri_json2psql(
        os.path.join(datadir, 'corporatie_bezit', 'AFWC_2017.json'),
        pg_str,
        'gas_afwc2017'
    )

    # energie labels (van maps.amsterdam.nl open geodata)
    esri_json2psql(
        os.path.join(datadir, 'energie_labels', 'ENERGIE_LABELS.json'),
        pg_str,
        'gas_energie_labels'
    )


if __name__ == '__main__':
    desc = 'Upload gas transitie datasets into PostgreSQL.'
    parser = argparse.ArgumentParser(desc)
    parser.add_argument('datadir', type=str,
        help='Local data directory', nargs=1)
    args = parser.parse_args()
    main(args.datadir[0])
