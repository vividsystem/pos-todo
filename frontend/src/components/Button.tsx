import { JSX, ParentProps, splitProps } from "solid-js";

interface ButtonProps extends JSX.ButtonHTMLAttributes<HTMLButtonElement> {
}
export default function Button(props: ParentProps<ButtonProps>) {
	const [_, buttonProps] = splitProps(props, ["children"])
	return (
		<button class="p-2 text-2xl bg-orange-700 text-orange-200 rounded-sm" {...buttonProps}>
			{props.children}
		</button>
	)
}
