import unittest
from abc import ABC

from src.plugin_loader import PluginLoader


class PluginTest(unittest.TestCase, ABC):

    @staticmethod
    def get_test_obj(name: str):
        loader = PluginLoader([{'name': name}])
        return loader.get_plugin(name)

    @staticmethod
    def get_test_obj_name():
        raise NotImplementedError()

    @staticmethod
    def tests():
        raise NotImplementedError()

