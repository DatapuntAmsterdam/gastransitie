from rest_framework_gis.serializers import GeoFeatureModelSerializer
from datasets.models import GasAfwc2017
from datasets.models import BagBuurt


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
