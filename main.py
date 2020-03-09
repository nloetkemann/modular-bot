import logging

from src.config import config
from src.plugin_loader import PluginLoader
from src.plugin_handler import PluginHandler
from src.tools.function_thread import FunctionThread

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)
threads = {}

if __name__ == '__main__':
    loader = PluginLoader(config.plugins)
    handler = PluginHandler(loader.get_plugins())

    for key in config.bots:
        thread = FunctionThread(config.bots[key].run, [handler])
        thread.start()
        threads[key] = thread

        thread.stop()
