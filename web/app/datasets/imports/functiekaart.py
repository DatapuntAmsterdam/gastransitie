import os

from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import esri_json2psql


def import_functiekaart(datadir):
    # Functiekaart (van maps.amsterdam.nl)
    pg_str = get_ogr2ogr_pgstr()
    esri_json2psql(
        os.path.join(datadir, 'functiekaart', 'FUNCTIEKAART.json'),
        pg_str,
        'niet_woon_functiekaart_raw'
    )
