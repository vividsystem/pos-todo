import { createContext } from "solid-js";
import { createStore } from "solid-js/store";

const settingsStore = createStore<{ header: string, footer: string }>({
	header: "",
	footer: ""
})

export const SettingsContext = createContext(settingsStore)
