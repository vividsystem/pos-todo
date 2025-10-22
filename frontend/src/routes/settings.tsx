import { useContext } from "solid-js";
import TextArea from "~/components/TextArea";
import { SettingsContext } from "~/lib/context/settings";

export default function SettingsPage() {
	const [settings, setSettings] = useContext(SettingsContext);
	return (
		<main class="text-center mx-auto p-4 flex flex-col items-start">
			<h1 class="text-2xl">Settings</h1>
			<div class="flex flex-col lg:flex-row gap-2">
				<TextArea
					label={"Header"}
					placeholder="Your header goes here..."
					cols={36}
					onInput={(ev) => ev.currentTarget.value !== "" ? setSettings("header", ev.currentTarget.value) : undefined}
				/>
				<TextArea
					label={"Footer"}
					placeholder="Your footer goes here..."
					cols={36}
					onInput={(ev) => ev.currentTarget.value !== "" ? setSettings("footer", ev.currentTarget.value) : undefined}
				/>
			</div>
		</main>
	)
}
