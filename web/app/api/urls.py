from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import GasAfwc2017ViewSet
from .views import BagBuurtViewSet

router = DefaultRouter()
router.register('afwc', GasAfwc2017ViewSet, base_name='afwc')
router.register('buurt', BagBuurtViewSet, base_name='buurt')

urlpatterns = router.urls
