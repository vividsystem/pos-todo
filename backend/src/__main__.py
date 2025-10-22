from cfg import Settings
from mqtt import client, initialize
from printer import Printer
import logging


if __name__ == "__main__":
    s = Settings()
    logging.basicConfig(level=logging.DEBUG)

    client.enable_logger()
    client.user_data_set(Printer(s))
    client.connect(s.mqtt.host, s.mqtt.port)
    initialize()
    client.loop_forever()
