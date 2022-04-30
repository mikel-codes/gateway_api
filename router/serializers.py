from rest_framework.serializers import ValidationError, ModelSerializer, CharField
from .models import Gateway, Device

class DeviceSerializer(ModelSerializer):
    """ Converts the Device Python Object to JSON """
    status_name = CharField(source="get_status_display", read_only=True, required=False)
    class Meta:
        model = Device
        fields = ("id", "gateway", "uid", "status", "created_on", "vendor", "status_name")
        read_only_fields = ("id", "status", "uid")


class GatewaySerializer(ModelSerializer):
    """ Converts the Gateway Python Object to JSON """

    class Meta:
        model = Gateway
        fields = ("id", "name", "serial", "ipv4", "device_set")
        read_only_fields = ("id", )

    def to_representation(self, value):
        repr = super().to_representation(value)
        repr['devices'] = DeviceSerializer(value.device_set, many=True, source="device_set").data #json -> FK(many=True)
        return repr
