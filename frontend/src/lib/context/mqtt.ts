import mqtt from "mqtt";
import { createContext } from "solid-js";
import { createStore, SetStoreFunction } from "solid-js/store";


const [status, setStatus] = createStore<object[]>([])
// TODO: maybe move to server?
const client = mqtt.connect(import.meta.env.VITE_MQTT_SERVER)
client.on("connect", () => {
	client.subscribe("pos-todo/status", (err) => {
		if (err) {
			console.log("an error occured trying to connect to pos-todo/status: ", err)
		} else {
			console.log("successfully connected to pos-todo/status")
		}
	})
})

client.on("message", (topic, message) => {
	if (topic === "pos-todo/status") {
		let msg = JSON.parse(message.toString())
		setStatus((prev) => [...prev, msg])
	}
})

interface IMQTTContext {
	client: mqtt.MqttClient,
	status: [object[], SetStoreFunction<object[]>]
}

export const MQTTContext = createContext({ client: client, statusStore: [status, setStatus] })
