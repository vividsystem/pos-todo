from escpos.printer import Network, Usb
from printer.options import TextOptions
from cfg import Settings


class Printer:
    def __init__(self, settings: Settings) -> None:
        self.text_width = 36
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
        self.driver.textln(self._insertln(line))

    def _insertln(self, text: str):
        lines = []
        current = ""
        for word in text.split():
            while len(word) > self.text_width:
                part = word[: self.text_width - 1] + "-"
                word = word[self.text_width - 1 :]
                if current:
                    # removes only trailing whitespaces
                    # -> dont break intentional indentation
                    lines.append(current.rstrip())
                    current = ""
                lines.append(part)

            if not current:
                current = word
            elif len(current) + len(word) <= self.text_width:
                current += " " + word
            else:
                lines.append(current.rstrip())
                current = word
        if current:
            lines.append(current.rstrip())

        return "\n".join(lines)

    def _ln(self, n: int = 1) -> None:
        self.driver.ln(n)

    def _printBlock(self, block: str, col: int) -> None:
        self.driver.textblock(block, col)

    def _reset(self) -> None:
        self.driver.set_with_default()

    def printMessage(self, header: str, content: str, footer: str) -> None:
        self._printLine("--" * 15)
        self._ln()
        TextOptions(bold=True, underlineType=2).set(self.driver)
        self._printLine(header)
        self._reset()
        self._ln()
        self._printLine(content)
        self._ln(2)
        self._printLine(footer)
        TextOptions(align="center").set(self.driver)
        self._ln()
        self._printLine("--" * 15)
        self._ln(8)
