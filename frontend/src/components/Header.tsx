import { A } from "@solidjs/router";
import { Cog } from "lucide-solid";

export default function Header() {
	return (
		<header class="static top-0 left-0 right-0 flex flex-row p-4 items-center justify-between">
			<h1 class="text-3xl">pos-todo</h1>
			<A href="/settings"><Cog class="size-8" /></A>
		</header >
	)
}
