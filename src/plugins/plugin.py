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
        """:param name the name of the plugin"""
        self.name = name
        self.config = config

    def get_method(self, method_name):
        """:return the method from from the name"""
        assert isinstance(method_name, str)
        return getattr(self, method_name)

