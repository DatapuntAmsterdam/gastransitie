import os
import tempfile

from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import run_command_sync
from datasets.imports.util import SRS_TO_STORE


def _load_eigendomskaart_mapinfo(
        zip_filename, pg_str, tab_filename, layer_name, **kwargs):

    with tempfile.TemporaryDirectory() as tempdir:
        cmd = ['unzip', '-d', tempdir, zip_filename]
        run_command_sync(cmd)

        # Load mapinfo file, we have an encoding problem here -skipfailures
        # allows us to continue in the presence of these encoding errors (about
        # 20 out of a total number of records of 500000.
        cmd = ['ogr2ogr', '-skipfailures', '-nln', layer_name]
        if 't_srs' in kwargs:
            cmd.extend(['-t_srs', kwargs['t_srs']])

        cmd.extend(
            ['-F', 'PostgreSQL', pg_str, os.path.join(tempdir, tab_filename)])

        run_command_sync(cmd)


def import_eigendomskaart(datadir):
    # Eigendomskaart
    pg_str = get_ogr2ogr_pgstr()
    _load_eigendomskaart_mapinfo(
        os.path.join(datadir, 'eigendomskaart', 'mapinfo.zip'),
        pg_str,
        os.path.join('mapinfo', 'kot_eig_adam.tab'),
        layer_name='kot_eig_adam_raw',
        t_srs=SRS_TO_STORE,
    )

    _load_eigendomskaart_mapinfo(
        os.path.join(datadir, 'eigendomskaart', 'mapinfo.zip'),
        pg_str,
        os.path.join('mapinfo', 'kot_eig_cat.tab'),
        layer_name='kot_eig_cat_raw',
        t_srs=SRS_TO_STORE,
    )
