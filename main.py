from src.config import config
from src.exceptions.not_found_exception import NotFoundException
from src.plugin_loader import PluginLoader
from src.plugin_handler import PluginHandler

if __name__ == '__main__':
    loader = PluginLoader(config.plugins)
    handler = PluginHandler(loader.get_plugins())

    text = input("Bitte mach eine Eingabe: ")

    try:
        plugin, method, foundparams = handler.validate_user_input(text)
        print(plugin.call_method(method, foundparams))
    except TypeError as t:
        print('Error: ich weiß nicht was ich machen soll')
        print(t)
    except NotFoundException as n:
        print('Es gab einen Fehler')
        exit(n)
