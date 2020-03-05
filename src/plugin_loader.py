# -----------------------------------------------------------
# a class to load all plugins from the yaml files
#
# 2020 Nikita Lötkemann, Rahden, Germany
# email n.loetkemann@fh-bielefeld.de
# -----------------------------------------------------------
import yamale
import yaml

from src.yaml.plugin import Plugin


class PluginLoader:
    def __init__(self, pluginlist, plugin_dir='./config/'):
        self.plugins = []
        for item in pluginlist:
            plugin_path = plugin_dir + item['name'] + '.yaml'
            with open(plugin_path, 'r') as config_file:
                self.validate_plugin_config(plugin_path)
                plugin_config = yaml.load(config_file)
                name = self.__first_upper(plugin_config['plugin']['name'])
                plugin = self.import_plugin(name)
                plugin = plugin(name, plugin_config['plugin'])
                assert isinstance(plugin, Plugin)
                self.plugins.append(plugin)

    def get_plugins(self):
        return self.plugins

    @staticmethod
    def __first_upper(word):
        return word[0].upper() + word[1:]

    @staticmethod
    def validate_plugin_config(path):
        schema = yamale.make_schema('./schemas/plugin-schema.yaml')
        data = yamale.make_data(path)
        try:
            yamale.validate(schema, data)
        except ValueError as e:
            print('Yaml file is mal formated. ' + path + '\n' + str(e))
            exit(1)

    @staticmethod
    def import_plugin(name): # todo add more safety code could be inserted in the loaded plugin
        return getattr(__import__('src.plugins.' + name.lower(), fromlist=[name]), name)
