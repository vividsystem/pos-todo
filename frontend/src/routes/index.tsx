import { useAction } from "@solidjs/router";
import { createSignal, useContext } from "solid-js";
import Button from "~/components/Button";
import TextArea from "~/components/TextArea";
import { SettingsContext } from "~/lib/context/settings";
import { printMessage as pM } from "~/server/mqtt";

export default function Home() {
	const [settings] = useContext(SettingsContext)
	const [message, setMessage] = createSignal("")

	const printMessage = useAction(pM)
	// column width might depend on printer. 42 chars works for TM88 III
	return (
		<main class="text-center mx-auto p-4 flex flex-col items-center justify-center">
			<div class="flex flex-col items-start">
				<TextArea label={"Message"} placeholder="Your message goes here..." onInput={(ev) => setMessage(ev.currentTarget.value)} cols={42} value={message()} />
				<Button onClick={async (ev) => {
					ev.preventDefault()
					await printMessage(message(), settings.header, settings.footer)
					setMessage("")
				}}>Print!</Button>
			</div>
		</main>
	);
}
