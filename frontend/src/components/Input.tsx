import { JSX, splitProps } from "solid-js"

interface InputProps extends JSX.InputHTMLAttributes<HTMLInputElement> {
	label: JSX.Element
}

export default function Input(props: InputProps) {
	const [_, inputProps] = splitProps(props, ["label"])
	return (
		<div class="flex flex-col justify-start items-start">
			<label class="text-xl pr-2 py-2">{props.label}</label>
			<input {...inputProps} />
		</div>
	)
}
