from src.config import config
from src.plugin_loader import PluginLoader
from src.plugin_handler import PluginHandler

loader = PluginLoader(config.plugins)
handler = PluginHandler(loader.get_plugins())
if __name__ == '__main__':
    text = input("Bitte mach eine Eingabe: ")

    try:
        plugin, method, foundparams = handler.validate_user_input(text)
        plugin.call_method(method, foundparams)
        plugin.answer(method, {})
    except TypeError as t:
        print('Error: ich weiß nicht was ich machen soll')
        print(t)

