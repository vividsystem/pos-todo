import type { App } from '@slack/bolt';
import { printingCallback } from './printing-command.js';

const register = (app: App) => {
	app.command('/pos-todo-print', printingCallback);
};

export default { register };
