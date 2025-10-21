from src.cfg import Settings
from src.printer import Printer
from src.printer.options import TextOptions


s = Settings()
p = Printer(s)


if __name__ == "__main__":
    TextOptions("right").set(p.driver)
    p.driver.textln("right aligned text")
    p._reset()

    for i in range(3):
        TextOptions(underlineType=i).set(p.driver)
        p.driver.text(f"type {i}")

    p.driver.ln()
    p._reset()

    for i in ["a", "b"]:
        TextOptions(font=i).set(p.driver)
        p.driver.text(f"type {i}")

    p._reset()
    p.driver.ln()

    for i in range(9):
        TextOptions(density=i).set(p.driver)
        p.driver.text(f"density {i}")
