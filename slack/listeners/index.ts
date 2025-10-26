import type { App } from '@slack/bolt';

import commands from './commands/index.js';
import shortcuts from './shortcuts/index.js';

const registerListeners = (app: App) => {
	commands.register(app);
	shortcuts.register(app);
};

export default registerListeners;
