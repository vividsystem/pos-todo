from escpos.escpos import Escpos
from escpos.printer import Network, Usb

from cfg import Settings


class Printer:
    def __init__(self, settings: Settings) -> None:
        if settings.connection == "USB" and settings.usb:
            self.driver = Usb(settings.usb.vendor_id, settings.usb.product_id, profile=settings.profile)
        elif settings.connection == "NETWORK" and settings.network:
            self.driver = Network(settings.network.ip, profile=settings.profile)
