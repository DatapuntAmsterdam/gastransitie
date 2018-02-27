from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import SerializerMethodField
from datasets.models import GasAfwc2017
from datasets.models import BagBuurt
from datasets.models import Mip2016
from datasets.models import EnergieLabel
from datasets.models import Renovatie


class GasAfwc2017Serializer(GeoFeatureModelSerializer):
    class Meta:
        model = GasAfwc2017
        fields = '__all__'

        geo_field = 'wkb_geometry'


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


class RenovatieSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Renovatie
        fields = '__all__'

        geo_field = 'wkb_geometry'


class BagBuurtBboxSerializer(GeoFeatureModelSerializer):
    bbox = SerializerMethodField()

    class Meta:
        model = BagBuurt
        fields = ('vollcode','bbox')

        geo_field = 'bbox'

    def get_bbox(self, obj):
        if obj.geometrie:
            return obj.geometrie.extent
