"use server"
import { action } from "@solidjs/router";
import mqtt from "mqtt";

const client = mqtt.connect(process.env.MQTT_SERVER!)

client.on("error", (e) => {
	console.error(e)

})

client.on("connect", () => {
	console.log(`connected successfully to ${process.env.MQTT_SERVER}`)
	client.subscribe("pos-todo/status", (err) => {
		if (err) {
			console.log("an error occured trying to connect to pos-todo/status: ", err)
		} else {
			console.log("successfully connected to pos-todo/status")
		}
	})
})


export const printMessage = action(async (message: string, header: string, footer: string) => {
	"use server"
	return await client.publishAsync("pos-todo/print/markdown", JSON.stringify({
		message,
		header,
		footer
	}))
}, "printMessage")

