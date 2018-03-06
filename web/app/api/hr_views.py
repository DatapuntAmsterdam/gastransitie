
from rest_framework import viewsets

# from .serializers import BagBuurtHRSerializer
from .serializers import HandelsregisterSerializer
from .serializers import HandelsregisterBuurtSerializer

from datasets.models import Handelsregister
from datasets.models import HandelsregisterBuurt


class HandelsregisterViewSet(viewsets.ModelViewSet):
    """
    Amsterdam Handelsregister gegevens per buurt
    """
    serializer_class = HandelsregisterSerializer
    # filter_class = GasAfwc2017Filter
    queryset = Handelsregister.objects.all().order_by('id')

    filter_fields = (
        'buurt_id', 'buurt_naam',
    )


class HandelsregisterBuurtViewSet(viewsets.ModelViewSet):
    """
    Amsterdam Handelsregister rapport per buurt
    """
    serializer_class = HandelsregisterBuurtSerializer
    queryset = HandelsregisterBuurt.objects.all().order_by('id')

    filter_fields = (
        'buurt_id', 'buurt_naam',
    )
