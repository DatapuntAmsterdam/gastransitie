from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('status/', include('health.urls')),
    path('gastransitie/api/', include('api.urls')),
    path('gastransitie/', include('web.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
