from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

routing = DefaultRouter()
routing.register('gateways', GatewayApi, "gateways")
routing.register('devices', DevicesApi, "devices")


urlpatterns = [] + routing.urls
