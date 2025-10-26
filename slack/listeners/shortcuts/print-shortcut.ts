import type { MessageShortcut, Middleware, SlackShortcutMiddlewareArgs, StringIndexed } from '@slack/bolt';
import { printMessage } from '../../mqtt/mqtt.js';

type MessageShortcutArgs = SlackShortcutMiddlewareArgs & {
	shortcut: MessageShortcut
}
const printShortcut: Middleware<MessageShortcutArgs> = async ({
	ack,
	client,
	logger,
	payload,
	shortcut,
	respond,
}) => {
	try {
		await ack();
		console.log("user:", shortcut.user.username, shortcut.user.id)
		const res = await client.users.profile.get({ user: shortcut.user.id })

		if (!shortcut.message.text) {
			return await respond('Your message needs to contain text!')
		}
		if (!res.ok || !res.profile) {
			return await respond('An error occured trying to fetch your profile information!')
		}
		const name =
			res.profile.display_name_normalized
			?? (shortcut.user.username ? "UN: " + shortcut.user.username : undefined)
			?? "USERNAME NOT DEFINED";
		await printMessage(shortcut.message.text, { name, id: payload.user.id })
		await respond('Your message is being printed now!');
	} catch (error) {
		logger.error(error);
	}
};

export { printShortcut };
