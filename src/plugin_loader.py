# -----------------------------------------------------------
# a class to load all plugins from the yaml files
#
# 2020 Nikita Lötkemann, Rahden, Germany
# email n.loetkemann@fh-bielefeld.de
# -----------------------------------------------------------
import logging
import yamale
import yaml

from src.tools.tools import Tools
from src.yaml.plugin import Plugin

logger = logging.getLogger(__name__)


class PluginLoader:
    def __init__(self, pluginlist, plugin_dir='./config/'):
        self.plugins = []
        for item in pluginlist:
            plugin_path = plugin_dir + item['name'] + '.yaml'
            ok, error = Tools.validate_yaml('./schemas/plugin-schema.yaml', plugin_path)
            if ok:
                plugin_config = Tools.read_config_file(plugin_path)
                name = Tools.first_to_upper(plugin_config['plugin']['name'])
                plugin = self.import_plugin(name)
                plugin = plugin(name, plugin_config['plugin'])
                assert isinstance(plugin, Plugin)
                self.plugins.append(plugin)
            else:
                logger.error(error)
                exit(1)

    def get_plugins(self) -> list:
        return self.plugins

    @staticmethod
    def import_plugin(name):  # todo add more safety code could be inserted in the loaded plugin
        return getattr(__import__('src.plugins.' + name.lower(), fromlist=[name]), name)
