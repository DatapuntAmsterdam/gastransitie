from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import GasAfwc2017ViewSet

router = DefaultRouter()
router.register('afwc', GasAfwc2017ViewSet, base_name='afwc')

urlpatterns = router.urls
