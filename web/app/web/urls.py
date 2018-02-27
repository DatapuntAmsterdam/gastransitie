from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('openapi.yml', views.OpenAPIView.as_view(), name='openapi'),
]
