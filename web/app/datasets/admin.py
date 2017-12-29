from django.contrib.gis import admin
from datasets.models import GasAfwc2017

# Register your models here.


class GasAfwc2017Admin(admin.ModelAdmin):
    readonly_fields = (
        'ogc_fid',
        'corp',
        'corporatie',
        'bouwjaar',
        'aantal_adressen',
        'aantal_corporatie',
        'percentage_corporatie',
        'gemeente',
        'perc',
    )
    # 'wkb_geometry', not in list of readonly fields (will not show map)
    # TODO: change the js and openlayers admin templates to use the map
    # backgrounds provided by api.data.amsterdam.nl
    modifiable = False

admin.site.register(GasAfwc2017, GasAfwc2017Admin)
#admin.site.register(GasAfwc2017)
