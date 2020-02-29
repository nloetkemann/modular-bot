from jsonschema import validate


# -----------------------------------------------------------
# the abstract class for all plugins
#
# 2020 Nikita Lötkemann, Rahden, Germany
# email n.loetkemann@fh-bielefeld.de
# -----------------------------------------------------------


class Plugin:
    """The abstract class for all plugins.
    """

    def __init__(self, name, config):
        """:param name the name of the plugin-schema.yaml"""
        self.name = name
        self.config = config

    def get_method(self, method_name):
        """:return the method from from the name"""
        assert isinstance(method_name, str)
        return getattr(self, method_name)

    def get_answers(self, method_name):

        all_methods = self.config[self.name]['methods']
        for method in all_methods:
            if method.name == method_name:
                return method['answers']['list']
        return []
