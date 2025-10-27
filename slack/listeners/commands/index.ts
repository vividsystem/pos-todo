import type { App } from '@slack/bolt';
import { printingCallback } from './printing-command.js';

const register = (app: App) => {
	app.command('/pos-print', printingCallback);
};

export default { register };
