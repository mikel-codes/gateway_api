#your api tests lives here
import json
import pytest
from django.urls import reverse_lazy
from model_bakery import baker
from ..models import Gateway, Device

def test_device_without_gw_endpoint_for_creation(api, device_payload):
    res =  api.post(reverse_lazy('router_api:devices-list'), device_payload)
    assert res.status_code == 201
    content = json.loads(res.content)
    assert content.get('gateway') == None
    assert content.get('uid') == None
    assert content.get('status') == "off"
    assert content.get('status_name') == "offline"


def test_device_is_added_to_gateway(api, gateway, device):
    assert device.gateway is None
    d_json = device.__dict__.copy()
    d_json.pop('_state')
    d_json['gateway'] = gateway.id
    res = api.put(reverse_lazy("router_api:devices-detail", kwargs={"pk": device.id}), d_json, format="json")

    assert res.status_code == 200
    content = json.loads(res.content)
    assert content.get('gateway') is not None
    assert content.get('status')  == "on"
    assert content.get('uid') == gateway.device_set.count()


def test_device_is_removed_from_gateway(api, gateway):
    dev1 = baker.make(Device, vendor="Swiss", gateway=gateway)
    dev2 = baker.make(Device, vendor="Oasis", gateway=gateway)
    assert gateway.device_set.count() == 2
    d_json = dev1.__dict__.copy()
    d_json.pop('_state')
    d_json['gateway'] = None
    res = api.put(reverse_lazy("router_api:devices-detail", kwargs={"pk": dev1.id}), d_json, format="json")
    assert res.status_code == 200
    content = json.loads(res.content)
    assert content.get('gateway') is  None
    assert content.get('status')  == "off"
    assert content.get('uid') == None
    assert gateway.device_set.count() == 1

def test_gateway_has_a_maximum_of_10_devices(api, gateway):
    devs = baker.make(Device, gateway=gateway, _quantity=10)
    dev1  = baker.make(Device)

    d_json = dev1.__dict__.copy()
    d_json.pop('_state')
    d_json['gateway'] = gateway.id

    res = api.put(reverse_lazy("router_api:devices-detail", kwargs={"pk": dev1.id}), d_json, format="json")
    assert res.status_code == 400
    json_response = json.loads(res.content)
    assert 'gateway' in json_response
    assert json_response.get('gateway')[0] == "Limit(10) of connected devices reached"
    assert dev1.status == 'off'
    assert dev1.uid == None



def test_device_is_created_with_valid_json(api, device_payload, gateway):
    device_payload['gateway'] = gateway.id
    res = api.post(reverse_lazy("router_api:devices-list"),device_payload)
    assert res.status_code == 201
    content = json.loads(res.content)
    assert content.get('gateway') == 1
    assert content.get('uid') == gateway.device_set.count()
    assert content.get('status') == "on"
    assert content.get('status_name') == "online"

def test_gateway_deleted_does_not_destroy_connected_device_objects(api, gateway):
    devices = baker.make(Device, gateway=gateway, _quantity=3)
    res = api.delete(reverse_lazy("router_api:gateways-detail", kwargs={'pk': gateway.id}))
    import pdb; pdb.set_trace()


"""
def test_gateway_add_device(api, gateway, device):
    assert gateway.device_set.count() == 0
    assert device.status == "off"
    gw = gateway.__dict__.copy()
    dd = device
    device_ = Device.objects.get(id=device.id)
    assert device_.gateway == None
    gw.pop('_state')
    device_list =  [*gateway.device_set.all().values_list('id', flat=True)]
    device_list.append(device.id)
    gw['device_set'] = device_list
    #import pdb; pdb.set_trace()
    res = api.put(reverse_lazy('router_api:gateways-detail', kwargs={"pk": gateway.id}), gw)
    import pdb; pdb.set_trace()
    assert res.status_code == 200
    assert gateway.device_set.count() == 1
    #fixtures can not be changed they more of static object,
    #to see the changes in device we have to scout the test database
    device_obj = Device.objects.get(id=device.id)
    assert device_obj.gateway != None
    assert device_obj.status == "on"
    #assert device.uid ==  1




"""
