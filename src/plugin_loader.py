import yaml

from src.plugins.plugin import Plugin
from src.plugins.weather import Weather
from src.plugins.wiki import Wiki
from src.plugins.welcome import Welcome


class PluginLoader:
    def __init__(self, pluginlist, plugin_dir='./config/'):
        self.plugins = []
        for item in pluginlist:
            plugin_path = plugin_dir + item['name'] + '.yaml'
            with open(plugin_path, 'r') as config_file:
                plugin_config = yaml.load(config_file)
                name = self.__first_upper(plugin_config['plugin']['name'])
                plugin = eval(name)(name, plugin_config['plugin'])
                assert isinstance(plugin, Plugin)
                self.plugins.append(plugin)

    @staticmethod
    def __first_upper(word):
        return word[0].upper() + word[1:]
