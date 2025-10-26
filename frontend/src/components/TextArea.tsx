import { JSX, splitProps } from "solid-js";

interface TextAreaProps extends JSX.TextareaHTMLAttributes<HTMLTextAreaElement> {
	label: JSX.Element
}
export default function TextArea(props: TextAreaProps) {
	const [_, textareaProps] = splitProps(props, ["label"])

	return (
		<div class="flex flex-col justify-start items-start py-4">
			<label class="text-xl py-2 pr-2">{props.label}</label>
			<textarea class="h-48 sm:text-xs lg:text-md xl:text-xl text-orange-300 bg-orange-800 p-2 rounded-md lg:h-96" {...textareaProps} />
		</div>
	)
}
