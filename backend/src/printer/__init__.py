from escpos.escpos import Escpos
from escpos.printer import Network, Usb

from cfg import Settings


class Printer:
    def __init__(self, settings: Settings) -> None:
        if settings.connection == "USB" and settings.usb:
            self.driver = Usb(
                int(settings.usb.vendor_id, 16),
                int(settings.usb.product_id, 16),
                profile=settings.profile,
            )
        elif settings.connection == "NETWORK" and settings.network:
            self.driver = Network(settings.network.host, profile=settings.profile)

        self.driver.open(raise_not_found=True)

    def _printLine(self, line: str) -> None:
        self.driver.textln(line)

    def printMessage(self, header: str, content: str, footer: str) -> None:
        # print header
        # print content
        # print footer?
        self.driver.textln(header)
        self.driver.ln(2)
        self.driver.textln(content)
        self.driver.ln(2)
        self.driver.textln(footer)
        self.driver.cut()
