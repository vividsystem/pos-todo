import type { App } from '@slack/bolt';
import { printShortcut } from './print-shortcut.js';

const register = (app: App) => {
	app.shortcut({ callback_id: 'pos_todo_print', type: 'message_action' }, printShortcut);
};

export default { register };
