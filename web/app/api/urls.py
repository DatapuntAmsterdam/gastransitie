from django.conf.urls import url, include
from rest_framework import routers

from .views import GasAfwc2017ViewSet
from .views import BagBuurtViewSet
from .views import Mip2016ViewSet
from .views import EnergieLabelViewSet
from .views import RenovatieViewSet
from .views import BagBuurtBboxViewSet
from .views import WarmtekoudeViewSet
from .views import BagBuurtRapportViewSet
from .views import GasOranjeViewSet
from .views import GasGroenViewSet
from .views import VerbruikBuurtRapportViewSet

from .hr_views import HandelsregisterViewSet
from .hr_views import HandelsregisterBuurtViewSet


class EnergieTransitieAPI(routers.APIRootView):
    """
    Energietransitie API.

    Specifieke functionaliteit voor het Energie transitie dasboard.
    """

    def get_api_root_view(self, **kwargs):
        view = super().get_api_root_view(**kwargs)
        cls = view.cls

        class Gastransitie(cls):
            def get_view_name(self):
                return 'Energietransitie API'

        Gastransitie.__doc__ = self.__doc__
        return Gastransitie.as_view()


class ApiRouter(routers.DefaultRouter):
    """The main router"""
    APIRootView = EnergieTransitieAPI


router = ApiRouter()

router.register('afwc', GasAfwc2017ViewSet, base_name='afwc')
router.register('buurt', BagBuurtViewSet, base_name='buurt')
router.register('bag', BagBuurtRapportViewSet, base_name='bag')
router.register('mip', Mip2016ViewSet, base_name='mip')
router.register('energielabel', EnergieLabelViewSet, base_name='enegielabel')
router.register('renovatie', RenovatieViewSet, base_name='renovatie')
router.register('buurtbbox', BagBuurtBboxViewSet, base_name='buurtbbox')

router.register('handelsregister', HandelsregisterViewSet)
router.register('handelsregisterbuurt', HandelsregisterBuurtViewSet)
router.register('warmtekoude', WarmtekoudeViewSet)
router.register('gasoranje', GasOranjeViewSet)
router.register('gasgroen', GasGroenViewSet)
router.register('energieverbruik', VerbruikBuurtRapportViewSet)

urlpatterns = router.urls
