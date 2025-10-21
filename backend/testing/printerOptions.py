from src.cfg import Settings
from src.printer import Printer
from src.printer.options import TextOptions


s = Settings()
p = Printer(s)


if __name__ == "__main__":
    p.driver.block_text(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla laoreet risus ut varius hendrerit. Proin cursus mollis augue et vestibulum. Ut consequat dictum lacus facilisis tincidunt. Vestibulum nibh velit, semper vel elit semper, porta auctor purus. Vivamus aliquam risus posuere massa fermentum auctor at a neque. Pellentesque iaculis erat est, vel scelerisque elit convallis vestibulum. Pellentesque dignissim sodales nisl, et tincidunt odio faucibus vitae."
    )

    p.driver.ln()

    p.driver.text(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla laoreet risus ut varius hendrerit. Proin cursus mollis augue et vestibulum. Ut consequat dictum lacus facilisis tincidunt. Vestibulum nibh velit, semper vel elit semper, porta auctor purus. Vivamus aliquam risus posuere massa fermentum auctor at a neque. Pellentesque iaculis erat est, vel scelerisque elit convallis vestibulum. Pellentesque dignissim sodales nisl, et tincidunt odio faucibus vitae."
    )

    p.driver.ln()

    p.driver.qr("https://github.com/vividsystem/pos-todo")

    p.driver.ln()

    TextOptions("right").set(p.driver)
    p.driver.textln("right aligned text")
    p._reset()

    for i in range(0, 2):
        TextOptions(underlineType=i).set(p.driver)
        p.driver.text(f"type {i}")

    p.driver.ln()
    p._reset()

    for i in ["a", "b"]:
        TextOptions(font=i).set(p.driver)
        p.driver.text(f"type {i}")

    p._reset()
    p.driver.ln()

    for i in range(0, 8):
        TextOptions(density=i).set(p.driver)
        p.driver.text(f"density {i}")
