from escpos.printer import Network, Usb
from printer.options import TextOptions
from cfg import Settings
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from typing import Optional

MARKDOWN_OPTIONS = {
    "html": False,
    "linkify": False,
    "xhtmlOut": True,
    "breaks": False,
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
        node = SyntaxTreeNode(tokens)
        self._walk_markdown(node)

    def _walk_markdown(self, node: SyntaxTreeNode):
        match node.type:
            case "root":
                pass
            case "text":
                print(f"{node.type}: {node.content}")
            case "paragraph":
                print(f"{node.type}: {node.content}")
            case "bullet_list":
                print(f"{node.type}: {node.content}")
                pass
            case "ordered_list":
                print(f"{node.type}: {node.content}")
                pass
            case "list_item":
                print(f"{node.type}: {node.content}")
                pass
            case "link":
                print(f"{node.type}: {node.content}")
                pass
            case "heading":
                print(f"{node.type}: {node.content}")
                pass
            case "strong":
                print(f"{node.type}: {node.content}")
                pass
            case "code":
                print(f"{node.type}: {node.content}")
                pass
            case "fence":
                print(f"{node.type}: {node.content}")
                pass
            case _:
                print(f"unhandled markdown type {node.type}!")
                print(f"{node.type}: {node.content}")
        for child in node.children:
            self._walk_markdown(child)

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
        TextOptions(bold=True, underlineType=2).set(self.driver)
        self._print(header)
        self._reset()
        self._ln()
        self._print(content)
        self._ln(2)
        self._print(footer)
        TextOptions(align="center").set(self.driver)
        self._ln()
        self._print("--" * 15)
        self._ln(2)
