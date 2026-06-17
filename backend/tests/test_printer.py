import pytest
from types import SimpleNamespace
from unittest.mock import MagicMock
from printer import Printer


@pytest.fixture
def printer(monkeypatch):
    dummy_settings = SimpleNamespace(
        connection="USB", usb=None, network=None, profile=None
    )
    # Replace Usb and Network classes with dummy factories
    monkeypatch.setattr("printer.Usb", lambda *a, **k: MagicMock())
    monkeypatch.setattr("printer.Network", lambda *a, **k: MagicMock())

    p = Printer(dummy_settings)
    p.driver = MagicMock()
    p.text_width = 42
    return p


@pytest.mark.parametrize(
    "text,expected",
    [
        ("hello world", ["hello world"]),
        (
            "=" * 43,
            ["=" * 41 + "-", "=="],
        ),
    ],
)
def test_wrap_text(printer, text, expected):
    result = printer._wrap_text(text)
    assert result == expected



@pytest.mark.parametrize(
    "text,expected",
    [
        ("hello **world**", "hello world"),
        (
            "this is an **inline** that i hope is `nice` and _smooth_.\nlinks like [google](google.com) should also work!\nbut wait there are more things!",
            "this is an inline that i hope is [nice] and\nsmooth. links like google (google.com)\nshould also work! but wait there are more\nthings!",
        ),
        ("`hello` *world*. **this** is important", "[hello] world. this is important"),
    ],
)
def test_walk_markdown(printer, text, expected):
    calls: list[str] = []
    printer.driver.text.side_effect = lambda text: calls.append(text)
    printer.printMarkdown(text)

    assert "".join(calls) == expected
