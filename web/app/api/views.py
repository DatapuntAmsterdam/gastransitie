from rest_framework import viewsets

from .serializers import GasAfwc2017Serializer
from .serializers import BagBuurtSerializer
from .serializers import Mip2016Serializer
from .serializers import EnergieLabelSerializer
from .serializers import RenovatieSerializer
from datasets.models import GasAfwc2017
from datasets.models import BagBuurt
from datasets.models import Mip2016
from datasets.models import EnergieLabel
from datasets.models import Renovatie


class GasAfwc2017ViewSet(viewsets.ModelViewSet):
    serializer_class = GasAfwc2017Serializer

    def get_queryset(self):
        """
        Filter against buurt (neighborhood) specified in request.
        """
        # Retrieve neighborhood (no filtering if neighborhood cannot be found).
        buurt_code = self.request.query_params.get('buurt', None)
        try:
            buurt = BagBuurt.objects.get(vollcode=buurt_code)
        except:
            buurt = None

        qs = GasAfwc2017.objects.all().order_by('ogc_fid')
        if buurt is not None:
            qs = qs.filter(wkb_geometry__intersects=buurt.geometrie)

        return qs


class Mip2016ViewSet(viewsets.ModelViewSet):
    serializer_class = Mip2016Serializer

    def get_queryset(self):
        """
        Filter against buurt (neighborhood) specified in request.
        """
        # Retrieve neighborhood (no filtering if neighborhood cannot be found).
        buurt_code = self.request.query_params.get('buurt', None)
        try:
            buurt = BagBuurt.objects.get(vollcode=buurt_code)
        except:
            buurt = None

        qs = Mip2016.objects.all().order_by('ogc_fid')
        if buurt is not None:
            qs = qs.filter(wkb_geometry__intersects=buurt.geometrie)

        return qs


class EnergieLabelViewSet(viewsets.ModelViewSet):
    serializer_class = EnergieLabelSerializer

    def get_queryset(self):
        """
        Filter against buurt (neighborhood) specified in request.
        """
        # Retrieve neighborhood (no filtering if neighborhood cannot be found).
        buurt_code = self.request.query_params.get('buurt', None)
        try:
            buurt = BagBuurt.objects.get(vollcode=buurt_code)
        except:
            buurt = None

        qs = EnergieLabel.objects.all().order_by('ogc_fid')
        if buurt is not None:
            qs = qs.filter(wkb_geometry__intersects=buurt.geometrie)

        return qs


class RenovatieViewSet(viewsets.ModelViewSet):
    serializer_class = RenovatieSerializer

    def get_queryset(self):
        """
        Filter against buurt (neighborhood) specified in request.
        """
        # Retrieve neighborhood (no filtering if neighborhood cannot be found).
        buurt_code = self.request.query_params.get('buurt', None)
        try:
            buurt = BagBuurt.objects.get(vollcode=buurt_code)
        except:
            buurt = None

        qs = Renovatie.objects.all().order_by('ogc_fid')
        if buurt is not None:
            qs = qs.filter(wkb_geometry__intersects=buurt.geometrie)

        return qs


class BagBuurtViewSet(viewsets.ModelViewSet):
    serializer_class = BagBuurtSerializer
    queryset = BagBuurt.objects.all()
