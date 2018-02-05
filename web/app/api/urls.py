from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import GasAfwc2017ViewSet
from .views import BagBuurtViewSet
from .views import Mip2016ViewSet

router = DefaultRouter()
router.register('afwc', GasAfwc2017ViewSet, base_name='afwc')
router.register('buurt', BagBuurtViewSet, base_name='buurt')
router.register('mip', Mip2016ViewSet, base_name='mip')

urlpatterns = router.urls
