import pytest
from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from model_bakery import baker
from ..models import Gateway, Device
#settings.configure()
class GatewayTest(TestCase):
    def setUp(self):
        self.gateway = Gateway.objects.create(serial="92292889229000", name="gatewayX", ipv4="2.2.2.2")

    def test_gateway_is_created(self):
        assert Gateway.objects.count() == 1

    def test_gateway_obj_parsing(self):
        assert str(self.gateway) == '92292889229000 gatewayX'

    def test_gateway_serial_is_unique(self):
        with self.assertRaises(IntegrityError):
            obj, is_created = Gateway.objects.get_or_create(serial="92292889229000", name="gatewayII", ipv4="1.1.1.1")
            self.assertFalse(is_created, False)
        assert Gateway.objects.count() == 1



class DeviceTest(TestCase):
    def setUp(self):
        self.gateway = Gateway.objects.create(serial="92292889229000", name="gatewayIII", ipv4="2.2.2.2")
        self.device_with_gw = Device.objects.create(uid=3, gateway=self.gateway, vendor="Iphone", status="on")
        self.device_without_gw = Device.objects.create(uid=3, vendor="Samsung", status="on")
        self.gw =  Gateway.objects.create(serial="11132889229000", name="gatewayIX", ipv4="2.3.2.0")
        self.devices = baker.make(Device, gateway=self.gw, _quantity=10)
        self.device = baker.make(Device)



    def test_device_is_created(self):
        self.assertEqual(Device.objects.count(), 13)

    def test_device_with_gw_obj_parsing(self):
        assert str(self.device_with_gw) == "Iphone 222222 3 on"

    def test_device_with_gw_obj_parsing(self):
        assert str(self.device_without_gw) == f"Samsung {self.device_without_gw.created_on} off"

    def test_device_changes_when_connected_to_gateway(self):
        self.device_without_gw.gateway = self.gateway
        self.device_without_gw.save()
        assert self.device_without_gw.uid == self.gateway.device_set.count()
        assert self.device_without_gw.status == "on"
        assert str(self.device_without_gw) == f"Samsung 222222 {self.device_without_gw.uid} on"


    def test_device_maximum_on_one_gateway(self):
        """
        it is rational to use this approach because the business logic
        describes the connection is made by device to gateway
        """
        assert len(self.gw.device_set.all()) == 10
        with self.assertRaisesRegex(ValidationError, "['Maximum (10) of connected devices reached']"):
            self.device.gateway = self.gw
            self.device.save()
