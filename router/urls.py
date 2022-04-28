from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

routing = DefaultRouter()
routing.register('gateways', GatewayApi, "gateways")
routing.register('devices', DeviceApi, "devices")


urlpatterns = [] + routing.urls
