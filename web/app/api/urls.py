from django.conf.urls import url, include
from rest_framework import routers

from .views import GasAfwc2017ViewSet
from .views import BagBuurtViewSet
from .views import Mip2016ViewSet
from .views import EnergieLabelViewSet
from .views import RenovatieViewSet
from .views import BagBuurtBboxViewSet


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
router.register('mip', Mip2016ViewSet, base_name='mip')
router.register('energielabel', EnergieLabelViewSet, base_name='enegielabel')
router.register('renovatie', RenovatieViewSet, base_name='renovatie')

router.register('buurtbbox', BagBuurtBboxViewSet, base_name='buurtbbox')

urlpatterns = router.urls
