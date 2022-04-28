from rest_framework.serializers import ValidationError, ModelSerializer
from .models import Gateway, Device

class DeviceSerializer(ModelSerializer):
    """ Converts the Device Python Object to JSON """
    class Meta:
        model = Device
        fields = ("id", "gateway", "uid", "created_on", "vendor")

class GatewaySerializer(ModelSerializer):
    """ Converts the Gateway Python Object to JSON """
    devices = DeviceSerializer(many=True, read_only=True) #json -> FK(many=True)
    class Meta:
        model = Gateway
        fields = ("id", "name", "ipv4", "devices")

    def validate(self, data):
        if self.id and len(self.devices) == 10:
            raise ValidationError("maximum limit of connected devices reached")
        return super().validate(data)
