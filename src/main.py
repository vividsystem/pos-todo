from escpos.printer import Usb

# Vendor ID and Product ID from dmesg
p = Usb(0x04b8, 0x0202)

p.text("Hello World!")
p.cut()
