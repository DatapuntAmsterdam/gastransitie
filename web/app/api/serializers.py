from rest_framework_gis.serializers import GeoFeatureModelSerializer
from datasets.models.corporatie_bezit import GasAfwc2017


class GasAfwc2017Serializer(GeoFeatureModelSerializer):
    class Meta:
        model = GasAfwc2017
        fields = '__all__'

        geo_field = "wkb_geometry"
