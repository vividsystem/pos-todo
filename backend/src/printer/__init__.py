from escpos.printer import Network, Usb
from printer.options import TextOptions
from printer.md import convert_markdown
from cfg import Settings


class Printer:
    def __init__(self, settings: Settings) -> None:
        self.text_width = 42
        if settings.connection == "USB" and settings.usb:
            self.driver = Usb(
                int(settings.usb.vendor_id, 16),
                int(settings.usb.product_id, 16),
                profile=settings.profile,
            )
            self.driver.open(raise_not_found=True)
        elif settings.connection == "NETWORK" and settings.network:
            self.driver = Network(settings.network.host, profile=settings.profile)
            self.driver.open(raise_not_found=True)

        self._n = 0

    def _print(self, text: str, improved_linebreaks: bool = True) -> None:
        if improved_linebreaks:
            text, _ = self._insertln(text)
            self.driver.textln(text)
        else:
            self.driver.textln(text)

    def printMarkdown(self, text_md: str, header: str, footer: str) -> None:
        exec = convert_markdown(header)
        for e in exec:
            if isinstance(e, str):
                self._printInline(e)
            else:
                e.set(self.driver)
        self._reset()
        self._ln()

        exec = convert_markdown(text_md)
        for e in exec:
            if isinstance(e, str):
                self._printInline(e)
            else:
                e.set(self.driver)

        self._reset()
        self._ln(2)
        exec = convert_markdown(footer)
        for e in exec:
            if isinstance(e, str):
                self._printInline(e)
            else:
                e.set(self.driver)

        TextOptions(align="center").set_default(self.driver)
        self._ln()
        self._hr()
        self._ln(2)
        self._reset()

    def _hr(self):
        self._print("-" * self.text_width)

    def _printInline(self, text: str):
        self.driver.text(text)

    def printQR(self, url: str):
        self.driver.qr(url)

    # 10.10.1.189
    def _insertln(self, text: str, offset: int = 0) -> (str, int):
        lines = self._wrap_text(text)
        return "\n".join(lines), len((lines[-1] if len(lines) != 0 else ""))

    def _wrap_text(self, text: str, offset: int = 0) -> list[str]:
        lines = []
        current = ""
        trailing = text.endswith(" ")
        starting = text.startswith(" ")
        old_offset = offset
        for word in text.split():
            if starting:
                word = " " + word
                starting = False

            while len(word) > self.text_width - offset:
                part = word[: self.text_width - offset - 1] + "-"
                word = word[self.text_width - offset - 1 :]
                offset = 0
                if current:
                    lines.append(current)
                    current = ""
                lines.append(part)

            if not current:
                current = word
            elif len(current) + len(word) <= self.text_width:
                current += " " + word
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)

        # TODO: fix cursed indents
        if lines and trailing:
            if old_offset > 0 and len(lines) == 1:
                if len(lines[0]) + old_offset < self.text_width:
                    lines[0] += " "
                else:
                    lines.append("")
            else:
                if len(lines[-1]) < self.text_width:
                    lines[-1] += " "
                else:
                    lines.append("")

        return lines

    def _ln(self, n: int = 1) -> None:
        self.driver.ln(n)

    def _reset(self) -> None:
        self.driver.set_with_default()

    def printMessage(self, header: str, content: str, footer: str) -> None:
        TextOptions(bold=True, underlineType=2).set_default(self.driver)
        self._print(header)
        self._reset()
        self._ln()
        self._print(content)
        self._ln(2)
        self._print(footer)
        TextOptions(align="center").set_default(self.driver)
        self._ln()
        self._print("--" * 15)
        self._ln(2)
        self._reset()
