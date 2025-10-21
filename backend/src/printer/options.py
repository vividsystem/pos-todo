from dataclasses import dataclass
from typing import Literal, Optional
from escpos import Escpos


@dataclass
class TextOptions:
    align: Literal["center", "left", "right"] = "left"
    font: Optional[Literal["a", "b"]] = None
    bold: bool = False
    underlineType: Optional[int] = None  # TODO replace
    height: Optional[int] = None  # 1-8
    width: Optional[int] = None  # 1-8
    density: Optional[int] = None  # 0-8
    invertColors: Optional[bool] = None
    smooth: Optional[bool] = None
    flipTextDirection: Optional[bool]

    def set(self, printer: Escpos):
        printer.set_with_default(
            align=self.align,
            font=self.font,
            bold=self.bold,
            underline=_clip(self.underlineType, 0, 2)
            if self.underlineType is not None
            else None,
            double_height=self.height == 2,
            double_width=self.width == 2,
            custom_size=self.width > 2 or self.height > 2,
            width=_clip(self.width, 1, 8) if self.width != 2 else None,
            height=_clip(self.height, 1, 8) if self.height != 2 else None,
            density=_clip(self.invertColors, 0, 8),
            invert=self.invertColors,
            smooth=(self.smooth if self.height >= 4 and self.width >= 4 else None),
            flip=self.flipTextDirection,
        )


def _clip(var: int, min: int, max: int):
    return min if var < min else max if var > max else var
