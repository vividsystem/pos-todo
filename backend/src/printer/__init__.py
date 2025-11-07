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

    def _print(self, text: str, improved_linebreaks: bool = True) -> None:
        if improved_linebreaks:
            self.driver.textln(self._insertln(text))
        else:
            self.driver.textln(text)

    def printMarkdown(
        self, text_md: str, header: Optional[str] = None, footer: Optional[str] = None
    ) -> None:
        tokens = self.md.parse(text_md)
        self._walk_markdown(tokens)

    def _hr(self):
        self._print("-" * 36)

    def _walk_markdown(self, tokens: list[Token]):
        list_stack = []
        for token in tokens:
            match token.type:
                case "paragraph_open":
                    pass
                case "paragraph_close":
                    self._ln()
                case "heading_open":
                    TextOptions(bold=True, underlineType=2).set(self)
                case "heading_close":
                    TextOptions(bold=False, underlineType=0).set(self)
                    self._ln()
                case "strong_open":
                    TextOptions(bold=True).set(self)
                case "strong_close":
                    TextOptions(bold=False).set(self)
                case "em_open":
                    TextOptions(underlineType=1).set(self)
                case "em_close":
                    TextOptions(underlineType=0).set(self)
                case "code_inline":
                    self._print(f"[{token.content}]")
                case "link_open":
                    url = token.attrGet("href")
                    print(f"lo_url: {url}")
                case "link_close":
                    url = token.attrGet("href")
                    print(f"lc_url: {url}")
                case "fence":
                    self._print(f"{(token.info or '') + ' '}Code")
                    self._ln()
                    self._print(f"{token.content}")
                    self._ln()
                    self._print("END OF CODE")
                case "bullet_list_open":
                    list_stack.append({"type": "bullet"})
                case "ordered_list_open":
                    order = int(token.attrs.get("order", 1)) if token.attrs else 1
                    list_stack.append({"type": "ordered", "number": order})
                case "bullet_list_close" | "ordered_list_close":
                    list_stack.pop()
                case "list_item_open":
                    if list_stack:
                        li = list_stack[-1]
                        prefix = "-"
                        if li["type"] == "ordered":
                            prefix = f"{li['number']}."
                            li["number"] += 1
                        self._print(prefix + " ")
                case "text":
                    self._print(token.content)
                case _:
                    print(f"{token.type} unknown")
        TextOptions().set_default(self)

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
