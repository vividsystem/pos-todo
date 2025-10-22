from escpos.escpos import Escpos
from escpos.printer import Network, Usb
from printer.options import TextOptions
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

    def _ln(self, n: int) -> None:
        self.driver.ln(n)

    def _printBlock(self, block: str, col: int) -> None:
        self.driver.textblock(block, col)

    def _reset(self) -> None:
        self.driver.set_with_default()

    def printMessage(self, header: str, content: str, footer: str) -> None:
        TextOptions(bold=True, underlineType=2).set(self.driver)
        self._printLine(header)
        self._reset()
        self._ln()
        self._printLine(content)
        self._ln(2)
        self._printLine(footer)
        TextOptions(align="center").set(self.driver)
        self._ln()
        self._printLine("---------")
        self._ln(5)
