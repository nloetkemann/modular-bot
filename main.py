from src.config import Config
from src.plugin_loader import PluginLoader
from src.plugins.plugin_handler import PluginHandler

plugins = []

if __name__ == '__main__':
    config = Config()
    loader = PluginLoader(config.plugins)

    first = loader.get_plugins()[0]

    text = 'wie ist das wetter in rahden um 2'

    handler = PluginHandler(loader.get_plugins())

    plugin, method, foundparams = handler.validate_user_input(text)

    print(plugin, method, foundparams)

    # print(first.get_answers('search_wiki'))
    #
    # print(first.get_methods())
    #
    # print(first.get_method('search_wiki'))
    #
    # print(first.get_keywords())
