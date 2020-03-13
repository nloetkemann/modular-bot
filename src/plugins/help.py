from src.yaml.plugin import Plugin
from src.config import config


class Help(Plugin):
    def general_help(self, args):
        plugins = []
        for plugin in config.get_plugins():
            method_help = {}
            for method in plugin.methods:
                help = plugin.get_method_attr(method).get_help()
                method_help[method] = help

            plugin_help = {'description': plugin.get_description(), 'methods': method_help, 'name': plugin.name}
            plugins.append(plugin_help)

        help = ''
        for plugin in plugins:
            help += '**{0}**\n{1}\n\n'.format(plugin['name'], plugin['description'])
            for method in plugin['methods']:
                help += '\n__{0}__:\n{1}'.format(str(method), str(plugin['methods'][method]))

        print(help)
        return {'$help': help}
