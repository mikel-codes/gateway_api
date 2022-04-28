from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here


class Gateway(models.Model):
    """ Represents a gateway of the router """
    serial = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=100)
    ipv4 = models.GenericIPAddressField(protocol="IPv4")

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
    gateway = models.ForeignKey("Gateway", on_delete=models.PROTECT)
    vendor = models.CharField(max_length=100)
    uid = models.BigIntegerField()
    status = models.CharField(choices=STATUSES, max_length=30)


    # TODO: Define fields here

    class Meta:
        """ Meta definition for Device."""

        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        """Unicode representation of Device."""
        return f'{self.gateway.name} {self.gateway.ipv4} {self.uid}'

    def save(self):
        """Save method for Device."""
        pass
