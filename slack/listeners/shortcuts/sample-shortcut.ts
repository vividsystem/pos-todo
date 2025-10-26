import type { AllMiddlewareArgs, SlackShortcutMiddlewareArgs } from '@slack/bolt';

const sampleShortcutCallback = async ({
	ack,
	client,
	logger,
	shortcut,
}: AllMiddlewareArgs & SlackShortcutMiddlewareArgs) => {
	try {

		await ack();
		console.log("shortcut!")
	} catch (error) {
		logger.error(error);
	}
};

export { sampleShortcutCallback };
