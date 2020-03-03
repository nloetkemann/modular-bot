from src.config import Config
from src.plugin_loader import PluginLoader
from src.plugin_handler import PluginHandler

config = Config()
loader = PluginLoader(config.plugins)
handler = PluginHandler(loader.get_plugins())
if __name__ == '__main__':
    text = input("Bitte mach eine Eingabe: ")

    try:
        plugin, method, foundparams = handler.validate_user_input(text)
    except TypeError as t:
        print('Error: ich weiß nci')

    plugin.call_method(method, foundparams)
