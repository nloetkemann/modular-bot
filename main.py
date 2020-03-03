from src.config import Config
from src.plugin_loader import PluginLoader
from src.plugin_handler import PluginHandler

config = Config()
loader = PluginLoader(config.plugins)
if __name__ == '__main__':
    text = input("Bitte mach eine Eingabe: ")

    handler = PluginHandler(loader.get_plugins())

    plugin, method, foundparams = handler.validate_user_input(text)

    print(plugin, method, foundparams)
