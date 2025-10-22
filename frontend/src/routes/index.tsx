import { createSignal, onMount, useContext } from "solid-js";
import Button from "~/components/Button";
import TextArea from "~/components/TextArea";
import { MQTTContext } from "~/lib/context/mqtt";
import ParticleBackground from "~/components/ParticleBackground";
import { Leaf } from "lucide-solid";
import IconGrid from "~/components/IconGrid";

export default function Home() {
	const { client, statusStore } = useContext(MQTTContext)
	const [status, setStatus] = statusStore
	const [message, setMessage] = createSignal("")

	// column width might depend on printer. 36 chars works for TM88 III
	// TODO: make next line func that inserts a \n when a word doesn't fit in the rest of the line
	return (
		<main class="text-center mx-auto p-4 flex flex-col items-center justify-center">
			<div class="flex flex-col items-start">
				<TextArea label={"Message"} class="h-48 sm:text-xs lg:text-md xl:text-xl text-orange-300 bg-orange-800 p-2 rounded-md lg:h-96" placeholder="Your message goes here..." onInput={(ev) => setMessage(ev.currentTarget.value)} cols={36} />
				<Button value={message()} onClick={(ev) => {
					ev.preventDefault()
					client.publish("pos-todo/print/message", JSON.stringify({
						message: message(),
					}))
					setMessage("")

				}}>Print!</Button>
			</div>
		</main>
	);
}
