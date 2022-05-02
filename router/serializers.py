from rest_framework.serializers import ValidationError, ModelSerializer, CharField, SerializerMethodField
from .models import Gateway, Device

class DeviceSerializer(ModelSerializer):
    """ Converts the Device Python Object to JSON """
    status_name = CharField(source="get_status_display", read_only=True)
    class Meta:
        model = Device
        fields = ("id", "gateway", "uid", "status", "created_on", "vendor", "status_name")
        read_only_fields = ("id", "status", "uid", "status_name")

    def to_representation(self, value):
        repr = super().to_representation(value)
        if value.gateway is not None:
            gateway_data = GatewaySerializer(value.gateway).data
            gateway_data.pop('devices')
            gateway_data.pop('device_set')
            repr['gatewayx'] = gateway_data
        else:
            repr['gatewayx'] = None
        return repr

class IntermediarySerializer(ModelSerializer):
    """ Converts the Device Python Object to JSON """
    status_name = CharField(source="get_status_display", read_only=True)
    class Meta:
        model = Device
        fields = ("id", "uid", "status", "created_on", "vendor", "status_name")
        read_only_fields = ("id", "status", "uid", "status_name")




class GatewaySerializer(ModelSerializer):
    """ Converts the Gateway Python Object to JSON """

    class Meta:
        model = Gateway
        fields = ("id", "name", "serial", "ipv4", "device_set")
        read_only_fields = ("id","device_set")


    def to_representation(self, value):
        repr = super().to_representation(value)
        repr['devices'] = IntermediarySerializer(value.device_set, many=True, source="device_set").data #json -> FK(many=True)
        return repr
