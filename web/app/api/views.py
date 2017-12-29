from django.shortcuts import render

from rest_framework import viewsets

from .serializers import GasAfwc2017Serializer
from datasets.models import GasAfwc2017


class GasAfwc2017ViewSet(viewsets.ModelViewSet):
    serializer_class = GasAfwc2017Serializer
    queryset = GasAfwc2017.objects.all()
    # TODO: queryset must be filtered agains neighborhood
