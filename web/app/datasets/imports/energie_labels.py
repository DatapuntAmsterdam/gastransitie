import os


from datasets.imports.util import get_ogr2ogr_pgstr
from datasets.imports.util import esri_json2psql


def import_energie_labels(datadir):
    # energie labels (van maps.amsterdam.nl open geodata)
    pg_str = get_ogr2ogr_pgstr()
    esri_json2psql(
        os.path.join(datadir, 'energie_labels', 'ENERGIE_LABELS.json'),
        pg_str,
        'gas_energie_labels_raw',
        t_srs='EPSG:28992'
    )
