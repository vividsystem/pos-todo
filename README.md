# pos-todo
Print your ideas, todos, or whatever other text you like to a receipt printer!


Unfortunately I can't give anyone acces to my printer right now, because I need to figure out some networking-security stuff beforehand.
So watch this cool demo video to see the website working!
[cool frontend demo video here](https://hc-cdn.hel1.your-objectstorage.com/s/v3/8f13d6fc73214885a3d00f43c2b1ff3d57e945db_img_0923.mp4)


## Features
Print via a:
- (pretty fall-themed) website 
    -> supports customized footer and header
- slackbot to print slack messages
- Markdown support
- QR support in markdown via `[link](qr:url)`


## Hardware Requirements
- a computer/raspberry pi to run the webserver
- ESC/POS-compatible printer (connected to the previously mentioned computer)

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
Just copy this config to `./config/mosquitto.conf`
```conf
# Allow anonymous connections (for testing)
allow_anonymous true

# Persistence and data directories
persistence true
persistence_location /mosquitto/data/

# Logging
log_dest file /mosquitto/log/mosquitto.log

# Default MQTT listener
listener 1883

# WebSocket listener (optional)
listener 9001
protocol websockets
```
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
2. Add `VITE_MQTT_SERVER="mqtt://YOURMQTTHOST"` to `frontend/.env`
### Slack
1. Modify the manifest.json to have the correct name, etc.
2. add your slack tockens and auth to `slack/.env` like so:
```
SLACK_CLIENT_ID=YOURSLACKCLIENTID
SLACK_CLIENT_SECRET=YOURSLACKCLIENTSECRET
SLACK_SIGNING_SECRET=YOURSLACKSIGNINGSECRET
SLACK_APP_TOKEN=YOURSLACKAPPTOKEN
SLACK_BOT_TOKEN=YOURSLACKBOTTOKEN
MQTT_HOST="mqtt://YOURHOST:YOURPORT"
```
```bash
cd slack
bun i
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
```bash
bun run start
```

## Configuration (for the backend)
This file uses a `.env` in `backend/` file for configuration

| Field            | Type                  | Description                           | Required                         |
| ---------------- | --------------------- | ------------------------------------- | -------------------------------- |
| `PRINTER__PROFILE` | string                | [Printer profile](https://python-escpos.readthedocs.io/en/latest/printer_profiles/available-profiles.html) | No                               |
| `PRINTER__CONNECTION`     | `"USB"` \| `"NETWORK"` | Type of connection to the printer     | Yes                              |
| `PRINTER__USB__VENDOR_ID`  | hex-string (no `0x` prefix) | Vendor ID of the USB printer          | Required if `PRINTER__CONNECTION=USB`     |
| `PRINTER__USB__PRODUCT_ID` | hex-string (no `0x` prefix) | Product ID of the USB printer         | Required if `PRINTER__CONNECTION=USB`     |
| `PRINTER__NETWORK__IP`     | string                | IP address of the network printer     | Required if `PRINTER__CONNECTION=NETWORK` |


## Usage
- Go to the website 
- type `/pos-todo <xour text>` 
- or use the `Print to pos-todo` shortcut on an already sent slack mesage

## Acknowledgments
This project is only possible thanks to [python-escpos](https://github.com/python-escpos/python-escpos)! Go leave them a star. 


## License
This project is licensed under the MIT License (see [LICENSE](./LICENSE) or https://opensource.org/licenses/MIT)
