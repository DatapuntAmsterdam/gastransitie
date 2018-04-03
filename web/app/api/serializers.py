from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from datasets.models import GasAfwc2017
from datasets.models import BagBuurt
from datasets.models import BagRapport
from datasets.models import Mip2016
from datasets.models import EnergieLabel
from datasets.models import Renovatie
from datasets.models import Handelsregister
from datasets.models import HandelsregisterBuurt
from datasets.models import Warmtekoude
from datasets.models import GasGroen, GasOranje


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
        auto_bbox = True
        # bbox_geo_field = 'bbox_geometry'


class BagBuurtRapportSerializer(ModelSerializer):
    class Meta:
        model = BagRapport
        fields = '__all__'


class HandelsregisterSerializer(ModelSerializer):
    class Meta:
        model = Handelsregister
        fields = '__all__'


class HandelsregisterBuurtSerializer(ModelSerializer):
    class Meta:
        model = HandelsregisterBuurt
        fields = '__all__'


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
        fields = ('vollcode', 'bbox')

        geo_field = 'bbox'

    def get_bbox(self, obj):
        if obj.geometrie:
            return obj.geometrie.extent


class WarmtekoudeSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Warmtekoude
        fields = '__all__'

        geo_field = 'wkb_geometry'


class GasGroenSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = GasGroen
        fields = '__all__'

        geo_field = 'wkb_geometry'


class GasOranjeSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = GasOranje
        fields = '__all__'

        geo_field = 'wkb_geometry'
