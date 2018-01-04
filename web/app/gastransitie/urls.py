from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('gastransitie/admin/', admin.site.urls),
    path('status/', include('health.urls')),
    path('gastransitie/api/', include('api.urls')),
    path('gastransitie/dash/', include('web.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
