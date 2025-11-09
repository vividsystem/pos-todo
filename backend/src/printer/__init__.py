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
            text, offset = self._insertln(text)
            self.driver.textln(text)
        else:
            self.driver.textln(text)

    def printMarkdown(
        self, text_md: str, header: Optional[str] = None, footer: Optional[str] = None
    ) -> None:
        tokens = self.md.parse(text_md)
        return self._walk_markdown(tokens)

    def _hr(self):
        self._print("-" * self.text_width)

    def _printInline(self, text: str, offset: int):
        text = "X" * (offset - 1) + " " + text
        text, new_offset = self._insertln(text)
        text = text[offset:]
        self.driver.text(text)
        return new_offset

    def _handleInline(self, token: Token, prefix: str = ""):
        if not token.children:
            return

        current_text = "" + prefix
        offset = 0
        for child in token.children:
            match child.type:
                case "text":
                    current_text += child.content
                case "strong_open":
                    if current_text:
                        current_text += " "
                        offset = self._printInline(current_text, offset)
                        current_text = ""
                    TextOptions(bold=True).set(self.driver)
                case "strong_close":
                    TextOptions(bold=False).set(self.driver)
                case "em_open":
                    if current_text:
                        current_text += " "
                        offset = self._printInline(current_text, offset)
                        current_text = ""
                    TextOptions(underlineType=1).set(self.driver)
                case "em_close":
                    TextOptions(underlineType=0).set(self.driver)
                case "code_inline":
                    if current_text:
                        current_text += " "
                        offset = self._printInline(current_text, offset)
                        current_text = ""
                    current_text += f"[{child.content}] "
                case "link_open":
                    pass
                case "link_close":
                    url = child.attrGet("href")
                    if url:
                        current_text += f" ({url})"
                case "softbreak" | "hardbreak":
                    if current_text:
                        offset = self._printInline(current_text, offset)
                        current_text = ""

        if current_text:
            offset = self._printInline(current_text, offset)

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
            TextOptions().set_default(self.driver)

    def _insertln(self, text: str):
        lines = self._wrap_text(text)
        return "\n".join(lines), len(lines[-1])

    def _wrap_text(self, text: str):
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
