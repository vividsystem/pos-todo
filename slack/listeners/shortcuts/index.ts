import type { App } from '@slack/bolt';
import { sampleShortcutCallback } from './sample-shortcut.js';

const register = (app: App) => {
	app.shortcut('pos_todo_print', sampleShortcutCallback);
};

export default { register };
