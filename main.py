import logging
from src.config import config
from src.plugin_loader import PluginLoader
from src.plugin_handler import PluginHandler
from src.tools.bot_thread import BotThread

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
threads = {}

if __name__ == '__main__':
    loader = PluginLoader(config.plugins)
    handler = PluginHandler(loader.get_plugins())

    for key in config.bots:
        thread = BotThread(config.bots[key].start_bot, [handler])
        thread.start()
        threads[key] = thread
