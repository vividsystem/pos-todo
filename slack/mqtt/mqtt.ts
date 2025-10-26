import mqtt from "mqtt";


const client = mqtt.connect(process.env.MQTT_HOST!)

export async function printMessage(text: string, header: { name: string, id: string }) {
	client.publishAsync("pos-todo/print/message", JSON.stringify({
		message: text,
		header: `Message from ${header.name}(${header.id}):`,
		footer: `printed using pos-todo slack`
	}))
}
