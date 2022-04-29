from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_ipv4_address, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# Create your models here

def restrict_amount(value):
    if Device.objects.filter(gateway=value.id).count() >= 10:
        raise ValidationError('Limit(10) of connected devices reached')

class Gateway(models.Model):
    """ Represents a gateway of the router """
    serial = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=100)
    ipv4 = models.GenericIPAddressField(protocol="IPv4", validators=[validate_ipv4_address])

    class Meta:
        verbose_name = _("Gateway")
        verbose_name_plural = _("Gateways")

    def __str__(self):
        return f'{self.serial} {self.name}'



class Device(models.Model):
    """ Represents a single peripheral device."""

    STATUSES = (
        ("on", _("online")),
        ("off", _("offline"))
    )
    # in django this is the many -> one rel.
    """
        in order to treat each device as its own object I attached null, blank
        as this treats a device as existent without or with gateway connection

    """


    gateway = models.ForeignKey("Gateway", on_delete=models.PROTECT, validators=[restrict_amount,], null=True, blank=True )
    vendor = models.CharField(max_length=100)
    uid = models.BigIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(11)])
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    status = models.CharField(choices=STATUSES, max_length=30, default=_("off"))

    # TODO: Define fields here

    class Meta:
        """ Meta definition for Device."""

        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        """Unicode representation of Device."""
        if self.gateway is not None:
            return f'{self.vendor} {self.gateway.ipv4} {self.uid} {self.status}'
        return f'{self.vendor} {self.created_on} {self.status}'


    def save(self, *args, **kwargs):
        if self.gateway is not None:
            #print(f"{self.gateway.name} {len(self.gateway.device_set.all())}")
            if len(self.gateway.device_set.all()) >= 10:
                raise ValidationError("Maximum (10) of connected devices reached")
            self.status = "on"
            self.uid = self.gateway.device_set.count() + 1
        else:
            self.status = "off"
            self.uid = None
        return super().save(*args, **kwargs)
