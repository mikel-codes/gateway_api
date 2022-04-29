import pytest
from rest_framework.test import APITestCase, APIClient, URLPatternsTestCase
from ..models import Device, Gateway

@pytest.fixture
def device(db):
    return Device.objects.create(vendor="LG", )

@pytest.fixture
def twelve_devices(db):
    devices = baker.make(Device, _quantity=12)
    return devices

@pytest.fixture
def gateway(db, device):
    gateway = Gateway.objects.create(serial="92928722211", name="gatewayIII", ipv4="10.0.0.1")
    #gateway.device_set.add(device)
    return gateway

@pytest.fixture
def device_with_gw(db, gateway):
    return Device.objects.create(vendor="Google", gateway=gateway)

@pytest.fixture
def device_payload(db):
    return {"vendor": "Apple"}

@pytest.fixture
def gateway_payload(db):
    return {"serial": "992822111", "name": "Space Jamz", "ipv4":"9220"}


@pytest.fixture
def api(request):
    api =  APIClient()
    return api
