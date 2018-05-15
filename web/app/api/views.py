from rest_framework import viewsets

from .serializers import GasAfwc2017Serializer
from .serializers import BagBuurtSerializer
from .serializers import Mip2016Serializer
from .serializers import EnergieLabelSerializer
from .serializers import RenovatieSerializer
from .serializers import BagBuurtBboxSerializer
from .serializers import WarmtekoudeSerializer
from .serializers import BagBuurtRapportSerializer
from .serializers import GasOranjeSerializer, GasGroenSerializer

from datasets.models.corporatie_bezit import GasAfwc2017
from datasets.models.bag import BagBuurt
from datasets.models.bag import BagRapport
from datasets.models.mip import Mip2016
from datasets.models.alliander import VerbruikPerBuurt

from datasets.models.energie_labels import EnergieLabel
from datasets.models.renovaties import Renovatie
from datasets.models.warmtekoude import Warmtekoude
from datasets.models.warmtekoude import WarmtekoudeSimple
from datasets.models.alliander import GasGroen, GasOranje

from django.shortcuts import get_object_or_404

from django_filters.rest_framework import filters
from django_filters.rest_framework import FilterSet

from datapunt_api.rest import DatapuntViewSet

import logging

LOG = logging.getLogger(__name__)


class BuurtFilter():
    """
    Filter dataset on buurt.
    """

    def buurtcode_filter(self, qs, _name, value):

        try:
            buurt = BagBuurt.objects.get(vollcode=value)
        except BagBuurt.DoesNotExist:
            buurt = None

        if buurt is not None:
            qs = qs.filter(wkb_geometry__intersects=buurt.geometrie)

        return qs


class GasAfwc2017Filter(FilterSet, BuurtFilter):

    buurt = filters.CharFilter(
        label='buurt', method='buurtcode_filter')

    class Meta:
        model = GasAfwc2017
        fields = (
            'buurt',
        )


class GasAfwc2017ViewSet(viewsets.ModelViewSet):
    """
    Amsterdam Federate Woningbouw Coorporaties
    """
    serializer_class = GasAfwc2017Serializer
    filter_class = GasAfwc2017Filter
    queryset = GasAfwc2017.objects.all().order_by('ogc_fid')


class MipFilter(FilterSet, BuurtFilter):

    buurt = filters.CharFilter(
        label='buurt', method='buurtcode_filter')

    class Meta:
        model = Mip2016
        fields = (
            'buurt',
        )


class Mip2016ViewSet(viewsets.ModelViewSet):
    serializer_class = Mip2016Serializer
    filter_class = MipFilter
    queryset = Mip2016.objects.all().order_by('ogc_fid')


class EnergieLabelFilter(FilterSet, BuurtFilter):

    buurt = filters.CharFilter(
        label='buurt', method='buurtcode_filter')

    class Meta:
        model = EnergieLabel
        fields = (
            'buurt',
        )


class EnergieLabelViewSet(viewsets.ModelViewSet):
    serializer_class = EnergieLabelSerializer
    queryset = EnergieLabel.objects.all().order_by('ogc_fid')
    filter_class = EnergieLabelFilter


class BuurtNaamFilter():
    def buurtcode_filter(self, qs, _name, value):
        if value is not None:
            qs = qs.filter(buurt=value)
        return qs


class RenovatieFilter(FilterSet, BuurtNaamFilter):
    buurt = filters.CharFilter(
        label='buurt', method='buurtcode_filter')

    class Meta:
        model = Renovatie
        fields = (
            'buurt',
        )


class RenovatieViewSet(viewsets.ModelViewSet):
    serializer_class = RenovatieSerializer
    queryset = Renovatie.objects.all().order_by('ogc_fid')
    filter_class = RenovatieFilter


class BagBuurtRapportViewSet(DatapuntViewSet):
    serializer_class = BagBuurtRapportSerializer
    serializer_detail_class = BagBuurtRapportSerializer
    queryset = BagRapport.objects.all().order_by('id')
    filter_fields = ('vollcode', 'code', 'naam')

    def get_object(self):
        pk = self.kwargs['pk']
        if pk and len(pk) == 14:
            obj = get_object_or_404(BagRapport, pk=pk)
        if pk and len(pk) == 4:
            obj = get_object_or_404(BagRapport, vollcode=pk)
        if pk and len(pk) == 3:
            obj = get_object_or_404(BagRapport, code=pk)

        return obj


class VerbruikBuurtRapportViewSet(DatapuntViewSet):
    serializer_class = BagBuurtRapportSerializer
    serializer_detail_class = BagBuurtRapportSerializer
    queryset = VerbruikPerBuurt.objects.all().order_by('id')
    filter_fields = ('vollcode', 'naam')


class BagBuurtViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BagBuurtSerializer
    queryset = BagBuurt.objects.all().order_by('id')
    filter_fields = ('vollcode',)


class BagBuurtBboxViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BagBuurtBboxSerializer
    queryset = BagBuurt.objects.all().order_by('id')
    filter_fields = ('vollcode',)


class WarmtekoudeFilter(FilterSet, BuurtFilter):

    buurt = filters.CharFilter(
        label='buurt', method='buurtcode_filter')

    class Meta:
        model = Warmtekoude
        fields = (
            'buurt',
        )


class WarmtekoudeViewSet(viewsets.ModelViewSet):
    serializer_class = WarmtekoudeSerializer
    queryset = WarmtekoudeSimple.objects.all().order_by('selectie')
    # filter_class = WarmtekoudeFilter


class GasGroenFilter(FilterSet, BuurtFilter):
    buurt = filters.CharFilter(
        label='buurt', method='buurtcode_filter')

    class Meta:
        model = GasGroen
        fields = (
            'buurt',
        )


class GasGroenViewSet(viewsets.ModelViewSet):
    serializer_class = GasGroenSerializer
    queryset = GasGroen.objects.all().order_by('ogc_fid')
    filter_class = GasGroenFilter


class GasOranjeFilter(FilterSet, BuurtFilter):
    buurt = filters.CharFilter(
        label='buurt', method='buurtcode_filter')

    class Meta:
        model = GasOranje
        fields = (
            'buurt',
        )


class GasOranjeViewSet(viewsets.ModelViewSet):
    serializer_class = GasOranjeSerializer
    queryset = GasOranje.objects.all().order_by('ogc_fid')
    filter_class = GasOranjeFilter
