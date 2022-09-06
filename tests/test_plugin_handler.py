import unittest

from src.plugin_handler import PluginHandler
from src.plugin_loader import PluginLoader


class TestPluginHandler(unittest.TestCase):
    def test_validate_user_input(self):
        loader = PluginLoader([{'name': 'checklist'}])
        plugin_handler = PluginHandler(loader.get_plugins())
        plugin, method, params = plugin_handler.validate_user_input('erledige käse von einkaufsliste')
        self.assertEqual(plugin.name, 'Checklist')
        self.assertEqual(method, 'check_from_checklist')
