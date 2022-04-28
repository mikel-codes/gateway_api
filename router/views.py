from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import GatewaySerializer, DeviceSerializer
from .models import Gateway, Device

# Create your views here.
class GatewayApi(viewsets.ModelViewSet):
    """ automatically adds the CRUD endpoints for this basic gateway api"""
    serializer_class = GatewaySerializer
    permission_classes = ("AllowAny",)
    queryset = Gateway.objects.all()


class DeviceApi(viewsets.ModelViewSet):
    """ automatically adds the CRUD endpoints for this basic gateway api"""
    serializer_class = DeviceSerializer
    permission_classes = ("AllowAny",)
    queryset = Device.objects.all()
