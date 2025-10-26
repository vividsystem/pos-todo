import paho.mqtt.client as mqtt

from printer import Printer
import json
import datetime


client = mqtt.Client(client_id="pos-todo")


def initialize():
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.subscribe("pos-todo/print/#")


def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed: {str(mid)} {str(granted_qos)}")


def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.qos)} {str(msg.payload)}")


@client.topic_callback("pos-todo/print/message")
def on_message_print(client: mqtt.Client, userdata: Printer, message: mqtt.MQTTMessage):
    try:
        payload = json.loads(message.payload)
    except Exception:
        client.publish(
            "pos-todo/status",
            json.dumps({"status": "error", "message": "payload couldn't be parsed"}),
        )

    if "message" not in payload or not isinstance(payload["message"], str):
        client.publish(
            "pos-todo/status",
            json.dumps(
                {
                    "status": "error",
                    "message": "you have to specify a message in your payload",
                }
            ),
        )

    dt = datetime.datetime.now()
    header = f"{dt.isoformat(timespec='seconds')} - TODOs"
    header = """

                   .-'\\
                   \\:. \\
                   |:.  \\
                   /::'  \\
                __/:::.   \\
        _.-'-.'`  `'.-'`'._\\-"`"-'-,
     .`;    :      :     :      :   : `.
    / :     :      :                 :  \\
   /        :/\\          :   /\\ :   :  \\
  ;   :     /\\ \\   :     :  /\\ \\    :  ;
 .    :    /  \\ \\          /  \\ \\       .
 ;        /_)__\\ \\ :     :/_)__\\ \\  :   ;
;         `-----`' : ,   :`-----`'          ;
|    :      :       / \\         :     :    |
|                  / \\ \\ :            :   |
|    :      :     /___\\ \\:      :         |
|    :      :     `----`'       :           |
;        |;-.,__   :     :   __.-'|   :     ;
 ;    :  ||   \\ \\``/'---'\\`\\` /  ||     ;
  .    :  \\   \\_\\/       \\_\\/   // '  .
           \\'._    /\\     /\\ _.-'/   :  ;
    \\   :   `._`'-/ /\\._./ /\\  .'  :  /
     `\\  :     `-.\\/__\\__\\/_.;'   : /`
       `\\  '   :   :        :   :  /`
         `-`.__`        :   :__.'-`
               `-..`.__.'..-

pumpkin says:"""
    if "header" in payload and isinstance(payload["header"], str):
        header = payload["header"]

    footer = "sent with pos-todo"
    if "footer" in payload and isinstance(payload["footer"], str):
        footer = payload["footer"]

    print(f"print message: {payload['message']}")
    userdata.printMessage(header, payload["message"], footer)
    client.publish(
        "pos-todo/status",
        json.dumps(
            {
                "status": "success",
                "message": "message sent successfully",
                "content": {
                    "header": header,
                    "message": payload["message"],
                    "footer": footer,
                },
            }
        ),
    )
