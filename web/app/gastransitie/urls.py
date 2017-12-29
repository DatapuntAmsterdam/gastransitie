from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('gastransitie/admin/', admin.site.urls),
    path('status/', include('health.urls')),
    path('gastransitie/', include('api.urls')),
    path('gastransitie/dash/', include('web.urls')),
]
