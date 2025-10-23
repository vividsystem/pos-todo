# pos-todo
A simple web app to print your todos and messages directly to a POS Printer

[cool frontend demo video here](https://hc-cdn.hel1.your-objectstorage.com/s/v3/8f13d6fc73214885a3d00f43c2b1ff3d57e945db_img_0923.mp4)


## Features
- website and slackapp to print your messages to a receipt-printer

(slackapp isn't be deployed right now as I have to implement tunneling into my home network from the nest app which I cant do right now.)

## Hardware Requirements
- a computer/raspberry pi to run a webserver
- ESC/POS-compatible printer

## Software Requirements
### Backend
- python
- uv (recommended for easy setup and running)
- cups
### Frontend
- bun

## Installation
(for all instances the repo has to be cloned first)
### Backend
2. Setup a MQTT Server (you can use the docker compose for that)
3. Setup your POS-Printer
If you have a USB-Printer make a udev rule for it.
For that find out your product id and vendor id using for example `lsusb`
Then create a udev rule in `/etc/udev/rules.d/99-pos-todo.rules`
with this content:
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="<YOURVENDORID>", ATTRS{idProduct}=="<YOURPRODUCTID>", MODE="0664", GROUP="dialout"
```
make sure to replace `<YOURVENDORID>` and `<YOURPRODUCTID>` (do not use a `0x` prefix. just the hex number) with your actual ids.
after that do `sudo service udev restart` or `sudo udevadm control --reload` to restart udev

### Frontend
```bash
cd frontend
bun i
```
### Slack
1. Modify the manifest.json to have the correct request_url, names, etc.
2. add your slack tockens and auth to `slack/.env` like so:
```env
SLACK_CLIENT_ID=YOURSLACKCLIENTID
SLACK_CLIENT_SECRET=YOURSLACKCLIENTSECRET
SLACK_SIGNING_SECRET=YOURSLACKSIGNINGSECRET
SLACK_APP_TOKEN=YOURSLACKAPPTOKEN
SLACK_BOT_TOKEN=YOURSLACKBOTTOKEN
MQTT_HOST=YOURMQTTHOST
```

## Deploying
### Backend
```bash
cd backend
uv run src
```
### Frontend
```bash
cd frontend
```
For testing:
```
bun run dev
```
Otherwise:
```bash
bun run build
bun run start
```

### Slack
See [SLACK README](./slack/README.md)

## Configuration (for the backend)
This file uses a `.env` in `backend/` file for configuration

| Field            | Type                  | Description                           | Required                         |
| ---------------- | --------------------- | ------------------------------------- | -------------------------------- |
| `PRINTER__PROFILE` | string                | [Printer profile](https://python-escpos.readthedocs.io/en/latest/printer_profiles/available-profiles.html) | No                               |
| `PRINTER__CONNECTION`     | `"USB"` \| `"NETWORK"` | Type of connection to the printer     | Yes                              |
| `PRINTER__USB__VENDOR_ID`  | hex-string (no `0x` prefix) | Vendor ID of the USB printer          | Required if `PRINTER__CONNECTION=USB`     |
| `PRINTER__USB__PRODUCT_ID` | hex-string (no `0x` prefix) | Product ID of the USB printer         | Required if `PRINTER__CONNECTION=USB`     |
| `PRINTER__NETWORK__IP`     | string                | IP address of the network printer     | Required if `PRINTER__CONNECTION=NETWORK` |


## Acknowledgments
This project is only possible thanks to [python-escpos](https://github.com/python-escpos/python-escpos)! Go leave them a star. 


## License
This project is licensed under the MIT License (see [LICENSE](./LICENSE) or https://opensource.org/licenses/MIT)
