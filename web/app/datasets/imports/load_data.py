import logging

from datasets.imports.alliander import import_alliander
from datasets.imports.corporatie_bezit import import_corporatie_bezit
from datasets.imports.renovaties import import_renovaties
from datasets.imports.cbs import import_cbs
from datasets.imports.warmtekoude import import_warmtekoude
from datasets.imports.mip import import_mip
from datasets.imports.eigendomskaart import import_eigendomskaart
from datasets.imports.energie_labels import import_energie_labels
from datasets.imports.functiekaart import import_functiekaart

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def import_raw(datadir):
    """
    Run the first step in the import process (build raw database tables).
    """
    import_renovaties(datadir)
#    import_warmtekoude(datadir)
    import_mip(datadir)
    import_energie_labels(datadir)
    import_cbs(datadir)
    import_corporatie_bezit(datadir)
#    import_alliander(datadir)
#    import_eigendomskaart(datadir)
#    import_functiekaart(datadir)


def main(datadir):
    """
    Import datasets, run SQL to get clean tables for Django
    """
    import_raw(datadir)
