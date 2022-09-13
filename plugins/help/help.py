from src.yaml.plugin import Plugin
from src.config import config


class Help(Plugin):
    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)
        self.plugins = []
        for plugin in config.get_plugins():
            method_help = {}
            for method in plugin.methods:
                method_attr = plugin.get_method_attr(method)
                help_text = method_attr.get_help()
                params = method_attr.get_keywords().get_params()
                keywords = method_attr.get_keywords().get_list()
                all_keywords = []
                all_params = {}
                for param in params:
                    all_params[param.get_name()] = param.description

                for keyword in keywords:
                    all_keywords.append(keyword)
                method_help[method] = {'help': help_text, 'params': all_params, 'keywords': keywords}

            plugin_help = {
                'description': plugin.get_description(),
                'methods': method_help,
                'name': plugin.name
            }
            self.plugins.append(plugin_help)

    def general_help(self, args):
        help_text = ''
        for plugin in self.plugins:
            help_text += '\n*_{0}*_\n{1}'.format(plugin['name'].replace('_', '\_'), plugin['description'])
            for method in plugin['methods']:
                help_text += '\n**-> {0}**:\n{1}\n'.format(method, plugin['methods'][method]['help'])
        return {'$help': help_text, '__parser': 'Markdown'}

    def plugin_help(self, args):
        self.requiere_param(args, '$plugin')
        plugin_name = args['$plugin']
        for plugin in self.plugins:
            if plugin['name'].lower() == plugin_name.lower():
                help_text = '*_{0}*_\n{1}'.format(plugin['name'], plugin['description'])
                for method in plugin['methods']:
                    params = '\nHier die Parameter:'
                    for param in plugin['methods'][method]['params']:
                        params += '\n--> {0} => {1}'.format(param, plugin['methods'][method]['params'][param])
                    keywords = '\nHier die Schreibweisen:'
                    for keyword in plugin['methods'][method]['keywords']:
                        keywords += '\n--> {0}'.format(keyword)
                    help_text += '\n**-> {0}**:\n{1}\n{2}\n{3}'.format(method, plugin['methods'][method]['help'],
                                                                       keywords, params)

                return {'$help': help_text, '__parser': 'Markdown'}
        return {'$help': 'Zu dem Plugin **{0}** konnte ich keine Hilfe finden'.format(plugin_name)}

    def plugin_list(self, args):
        plugins = ''
        for plugin in self.plugins:
            plugins += '\n- {0}'.format(plugin['name'].replace('_', '\_'))

        return {'$list': plugins}
