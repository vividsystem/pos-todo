import { ParentProps } from "solid-js"
import { A } from "@solidjs/router"

interface LinkProps {
	href: string
}
export default function Link(props: ParentProps<LinkProps>) {
	return (
		<A href={props.href} class="underline">{props.children}</A >
	)
}
