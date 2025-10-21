# pos-todo
A simple web app to print your todos and messages directly to a POS Printer

## Features


## Hardware Requirements
- a computer/raspberry pi to run a webserver
- ESC/POS-compatible printer

## Software Requirements
- python
- uv (recommended for easy setup and running)


## Installation
1. Clone the repository
2. Setup a MQTT Server (you can use the docker compose for that)
3. Setup your POS-Printer
If you have a USB-Printer make a udev rule for it.
For that find out your product id and vendor id using for example `lsusb`
Then create a udev rule in `/etc/udev/rules.d/99-pos-todo.rules`
with this content:
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="<YOURVENDORID>", ATTRS{idProduct}=="<YOURPRODUCTID>", MODE="0664", GROUP="dialout"
```
make sure to replace `<YOURVENDORID>` and `<YOURPRODUCTID>` with your actual ids.
after that do `sudo service udev restart` or `sudo udevadm control --reload` to restart udev


## Usage 
```bash
uv run src
```

## Configuration
This file uses a `.env` file for configuration

| Field            | Type                  | Description                           | Required                         |
| ---------------- | --------------------- | ------------------------------------- | -------------------------------- |
| `PRINTER__PROFILE` | string                | [Printer profile](https://python-escpos.readthedocs.io/en/latest/printer_profiles/available-profiles.html) | No                               |
| `PRINTER__CONNECTION`     | `"USB"` \| `"NETWORK"` | Type of connection to the printer     | Yes                              |
| `PRINTER__USB__VENDOR_ID`  | string                | Vendor ID of the USB printer          | Required if `PRINTER__CONNECTION=USB`     |
| `PRINTER__USB__PRODUCT_ID` | string                | Product ID of the USB printer         | Required if `PRINTER__CONNECTION=USB`     |
| `PRINTER__NETWORK__IP`     | string                | IP address of the network printer     | Required if `PRINTER__CONNECTION=NETWORK` |


## Acknowledgments
This project is only possible thanks to [python-escpos](https://github.com/python-escpos/python-escpos)! Go leave them a star. 


## License
This project is licensed under the MIT License (see [LICENSE](./LICENSE) or https://opensource.org/licenses/MIT)
