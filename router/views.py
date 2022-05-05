from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import GatewaySerializer, DeviceSerializer
from .models import Gateway, Device

# Create your views here.
class GatewayApi(viewsets.ModelViewSet):
    """ automatically adds the CRUD endpoints for this basic gateway api"""
    serializer_class = GatewaySerializer
    permission_classes = (AllowAny,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["serial",]
    queryset = Gateway.objects.all()


class DeviceApi(viewsets.ModelViewSet):
    """ automatically adds the CRUD endpoints for this basic gateway api"""
    serializer_class = DeviceSerializer
    permission_classes = (AllowAny,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["vendor",]
    queryset = Device.objects.all()
