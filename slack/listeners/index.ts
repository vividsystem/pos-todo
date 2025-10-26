import type { App } from '@slack/bolt';

import commands from './commands/index.js';
import events from './events/index.js';
import messages from './messages/index.js';
import shortcuts from './shortcuts/index.js';

const registerListeners = (app: App) => {
	commands.register(app);
	events.register(app);
	messages.register(app);
	shortcuts.register(app);
};

export default registerListeners;
