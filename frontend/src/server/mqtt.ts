"use server";
import { action } from "@solidjs/router";
import mqtt from "mqtt";

// const [status, setStatus] = createStore<object[]>([])
const client = mqtt.connect(process.env.MQTT_SERVER!)

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

// client.on("message", (topic, message) => {
// 	if (topic === "pos-todo/status") {
// 		let msg = JSON.parse(message.toString())
// 		setStatus((prev) => [...prev, msg])
// 	}
// })


export const printMessage = action(async (message: string, header: string, footer: string) => {
	return await client.publishAsync("pos-todo/print/markdown", JSON.stringify({
		message,
		header,
		footer
	}))
}, "printMessage")

