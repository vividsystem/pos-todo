from escpos.printer import Network, Usb
from printer.options import TextOptions
from cfg import Settings
from markdown_it import MarkdownIt
from markdown_it.tree import Token
from typing import Optional

MARKDOWN_OPTIONS = {
    "html": False,
    "linkify": False,
    "xhtmlOut": True,
    "breaks": True,
    # "tyopgrapher": True,
    # quotes: "...",
    "components": {
        "core": {
            "normalize",
            "block",
            "inline",
            # "linkify",
            # "smartquotes"
            "text_join",
        },
        "block": {
            "rules": [
                "blockquote",
                "hr",
                "list",
                # "fence" -> ```code```
                # code -> ``
                "paragraph",
            ]
        },
        "inline": {
            "text",
            # "linkify",
            "escape",
            "backticks",
            # "strikethrough",
            # "emphasis" -> italics
            "link",
        },
        "inline2": ["balance_pairs", "fragments_join"],
    },
}


class Printer:
    def __init__(self, settings: Settings) -> None:
        self.md = MarkdownIt(options_update=MARKDOWN_OPTIONS)
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
        tokens_header = self.md.parse(header)
        self._walk_markdown(tokens_header)
        self._reset()
        self._ln()
        tokens_body = self.md.parse(text_md)
        self._walk_markdown(tokens_body)
        self._ln(2)
        tokens_footer = self.md.parse(footer)
        self._walk_markdown(tokens_footer)
        TextOptions(align="center").set_default(self.driver)
        self._ln()
        self._print("--" * 15)
        self._ln(2)

    def _hr(self):
        self._print("-" * self.text_width)

    def _printInline(self, text: str):
        self.driver.text(text)

    def printQR(self, url: str):
        self.driver.qr(url)

    def _handleInline(self, token: Token, prefix: str = ""):
        if not token.children:
            return

        url = ""
        qr = True

        text = prefix
        format_queue = [{"position": len(text), "to": TextOptions()}]
        offset = 0
        # todo add a qr code queue
        for child in token.children:
            match child.type:
                case "text":
                    tx, offset = self._insertln(child.content, offset)
                    text += tx
                case "strong_open":
                    format_queue.append(
                        {"position": len(text), "to": TextOptions(bold=True)}
                    )
                case "strong_close":
                    format_queue.append(
                        {"position": len(text), "to": TextOptions(bold=False)}
                    )
                case "em_open":
                    format_queue.append(
                        {"position": len(text), "to": TextOptions(underlineType=1)}
                    )
                case "em_close":
                    format_queue.append(
                        {"position": len(text), "to": TextOptions(underlineType=0)}
                    )
                case "code_inline":
                    tx, offset = self._insertln(f"[{child.content}]", offset)
                    text += tx

                case "link_open":
                    url = child.attrGet("href")
                    if url.startswith("qr:"):
                        qr = True
                        url = url[3:]
                case "link_close":
                    if url and not qr:
                        tx, offset = self._insertln(f"({url})", offset)
                        text += tx
                        url = ""
                    elif url and qr:
                        tx, offset = self._insertln(f"(see qr code or {url})", offset)
                        text += tx
                        self.printQR(url)
                        url = ""
                        qr = False
                case "softbreak":
                    pass
                case "hardbreak":
                    self._ln()

        for i in range(len(format_queue)):
            pos = format_queue[i]["position"]
            to: TextOptions = format_queue[i]["to"]
            to.set(self.driver)
            if i == len(format_queue) - 1:
                # print everything until the end
                self._printInline(text[pos:].rstrip())
            else:
                next_pos = format_queue[i + 1]["position"]
                self._printInline(text[pos:next_pos])
        self._reset()
        self._ln()

    def _handleBlockQuote(self, token: Token):
        pass

    def _walk_markdown(self, tokens: list[Token]):
        list_stack = []
        for token in tokens:
            match token.type:
                case "paragraph_open":
                    pass
                case "paragraph_close":
                    pass
                case "hr":
                    self._hr()
                case "inline":
                    prefix = ""
                    if list_stack:
                        li = list_stack[-1]
                        if li["type"] == "ordered":
                            prefix = f"{li['number']}. "
                        else:
                            prefix = "- "
                    self._handleInline(token, prefix)
                case "heading_open":
                    TextOptions(bold=True, underlineType=2).set(self.driver)
                case "heading_close":
                    TextOptions(bold=False, underlineType=0).set(self.driver)
                    self._ln()
                case "fence":
                    self._print(f"{(token.info or '') + ' '}Code")
                    self._print(f"{token.content}")
                    self._print("END OF CODE")
                case "bullet_list_open":
                    list_stack.append({"type": "bullet"})
                case "ordered_list_open":
                    order = int(token.attrs.get("order", 1)) if token.attrs else 1
                    list_stack.append({"type": "ordered", "number": order})
                case "bullet_list_close" | "ordered_list_close":
                    list_stack.pop()
                case "list_item_open":
                    pass
                case "list_item_close":
                    pass
                case _:
                    print(f"{token.type} unknown")
            self._reset()

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
