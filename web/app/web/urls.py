from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name="web/testkaart.html")),
    path('openapi.yml', views.OpenAPIView.as_view(), name='openapi'),
]
