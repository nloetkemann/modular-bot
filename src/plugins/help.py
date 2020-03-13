from src.yaml.plugin import Plugin
from src.config import config


class Help(Plugin):
    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)
        self.plugins = []
        for plugin in config.get_plugins():
            method_help = {}
            for method in plugin.methods:
                help_text = plugin.get_method_attr(method).get_help()
                method_help[method] = help_text

            plugin_help = {'description': plugin.get_description(), 'methods': method_help, 'name': plugin.name}
            self.plugins.append(plugin_help)

    def general_help(self, args):
        help_text = ''
        for plugin in self.plugins:
            help_text += '\n*_{0}*_\n{1}'.format(plugin['name'], plugin['description'])
            for method in plugin['methods']:
                help_text += '\n**-> {0}**:\n{1}\n'.format(method, plugin['methods'][method])
        return {'$help': help_text}
