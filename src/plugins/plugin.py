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

    def get_name(self):
        return self.name

    def get_method(self, method_name):
        for method in self.config['methods']:
            if method['name'] == method_name:
                return method

    def get_params_from_method(self, method_name):
        method = self.get_method(method_name)
        return method['keywords']['params'] if 'keywords' in method and 'params' in method['keywords'] else []

    def call_method(self, method_name):
        """:return the method from from the name"""
        assert isinstance(method_name, str)
        return getattr(self, method_name)

    def get_answers(self, method_name):
        return self.get_method(method_name)['answers']['list']


    def get_keywords(self):
        keywords = []
        for method in self.config['methods']:
            keywords.append(
                {
                    'name': method['name'],
                    'list': method['keywords']['list'],
                    'params': method['keywords']['params'] if 'params' in method['keywords'] else []
                })

        return keywords

    def get_method_names(self):
        all_methods = []
        for method in self.config['methods']:
            all_methods.append(method['name'])
        return all_methods
