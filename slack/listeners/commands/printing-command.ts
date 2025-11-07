import type { AllMiddlewareArgs, Middleware, SlackCommandMiddlewareArgs, StringIndexed } from '@slack/bolt';
import { printMessage } from '../../mqtt/mqtt.js';

const printingCallback: Middleware<SlackCommandMiddlewareArgs> = async ({ ack, respond, logger, payload, client }) => {
	try {
		await ack();
		const res = await client.users.profile.get({ user: payload.user_id })
		if (!res.ok || !res.profile) {
			await respond('An error occured trying to fetch your profile information!')
			return
		}
		const name = res.profile.display_name_normalized ?? "UN: " + payload.user_name;
		await printMessage(payload.text, { name, id: payload.user_id })
		await respond('Your message is being printed now!');
	} catch (error) {
		logger.error(error);
	}
};

export { printingCallback };
