# -----------------------------------------------------------
# the abstract class for all plugins
#
# 2020 Nikita Lötkemann, Rahden, Germany
# email n.loetkemann@fh-bielefeld.de
# -----------------------------------------------------------


class Plugin:
    """The abstract class for all plugins.
        :param name the name of the plugin
    """
    def __init__(self, name):
        self.name = name
