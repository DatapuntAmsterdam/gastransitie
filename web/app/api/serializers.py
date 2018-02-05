from rest_framework_gis.serializers import GeoFeatureModelSerializer
from datasets.models import GasAfwc2017
from datasets.models import BagBuurt
from datasets.models import Mip2016
from datasets.models import EnergieLabel


class GasAfwc2017Serializer(GeoFeatureModelSerializer):
    class Meta:
        model = GasAfwc2017
        fields = '__all__'

        geo_field = "wkb_geometry"


class BagBuurtSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = BagBuurt
        fields = '__all__'

        geo_field = 'geometrie'


class Mip2016Serializer(GeoFeatureModelSerializer):
    class Meta:
        model = Mip2016
        fields = '__all__'

        geo_field = "wkb_geometry"


class EnergieLabelSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = EnergieLabel
        fields = '__all__'

        geo_field = 'wkb_geometry'
