import { Github } from "lucide-solid";
import Link from "./Link";
import GithubIcon from "./GithubIcon";

export default function Footer() {
	return (
		<footer class="fixed bottom-0 left-0 right-0 flex flex-row items-center justify-between p-4 text-orange-800">
			<span>made by <Link href="https://github.com/vividsystem">vividsystem</Link></span>
			<Link href="https://github.com/vividsystem/pos-todo"><GithubIcon class="stroke-orange-800 fill-orange-800 size-8" /></Link>
		</footer>
	)
}
