import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";
import { Suspense } from "solid-js";
import "./app.css";
import Header from "./components/Header";
import Footer from "./components/Footer";

export default function App() {
	return (
		<Router
			root={props => (
				<div class="h-screen">
					<Header />
					<Suspense>{props.children}</Suspense>
					<Footer />
				</div>
			)}
		>
			<FileRoutes />
		</Router>
	);
}
