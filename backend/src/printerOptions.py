from cfg import Settings
from printer import Printer
from printer.options import TextOptions


s = Settings()
p = Printer(s)


if __name__ == "__main__":
    TextOptions("right").set(p.driver)
    p.driver.textln("right aligned text")
    p._reset()

    for i in range(3):
        TextOptions(underlineType=i).set(p.driver)
        p.driver.textln(f"type {i}")

    p.driver.ln()
    p._reset()

    for i in ["a", "b"]:
        TextOptions(font=i).set(p.driver)
        p.driver.textln(f"type {i}")

    p._reset()
    p.driver.ln()

    for i in range(9):
        TextOptions(density=i).set(p.driver)
        p.driver.textln(f"density {i}")

    p._reset()
    for i in range(1, 9):
        for j in range(1, 9):
            TextOptions(width=i, height=j)
            p.driver.textln(f"this text is printed with h={j} w={i}")

    p._reset()


# Findings
# when using .text() text doesnt wrap lines!
# -> always use textln
# font type b looks shitty
