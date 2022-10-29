import logging
from src.config import config
from src.plugin_loader import PluginLoader
from src.plugin_handler import PluginHandler
from src.tools.bot_thread import BotThread

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S ',
                    handlers=[logging.StreamHandler(), logging.FileHandler('./logs/log.txt', mode='w')])

logger = logging.getLogger(__name__)
threads = {}

if __name__ == '__main__':
    loader = PluginLoader(config.plugins)
    handler = PluginHandler(loader.get_plugins())

    for key in config.bots:
        thread = BotThread(config.bots[key].start_bot, [handler])
        thread.start()
        threads[key] = thread
