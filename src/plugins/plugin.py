# -----------------------------------------------------------
# the abstract class for all plugins
#
# 2020 Nikita Lötkemann, Rahden, Germany
# email n.loetkemann@fh-bielefeld.de
# -----------------------------------------------------------
from src.exceptions.not_found_exception import NotFoundException
from src.exceptions.token_exception import TokenException


class Plugin:
    """The abstract class for all plugins.
    """
    token_required = False
    token = ""

    def __init__(self, name, config):
        """:param name the name of the plugin-schema.yaml"""
        self.name = name
        self.config = config

        if self.token_required:
            self.require_token()

    def require_token(self):
        """
        should be called if a token is required
        this will be checked when calling the constuctor of the plugin
        :exception: TokenException if no token is set
        """
        if 'token' in self.config and self.config['token'] != '':
            self.token = self.config['token']
        else:
            raise TokenException('Wiki')

    def requiere_param(self, param, name):
        """
        should be called in the method of the plugin, checks if a parameter is set, which is requiered
        :param param: all params  of the method
        :param name: the name of the requiered param
        :exception: NotFoundException if the param is not set
        """
        if name not in param:
            raise NotFoundException('Parameter not found: {0}'.format(name))

    def get_name(self):
        """
        :return: the name of the plugin
        """
        return self.name

    def get_method(self, method_name):
        """
        gets the method from all methods by name
        :param method_name: the name
        :return: the method object {name: '', keywords: {}, answers: {}}
        """
        for method in self.config['methods']:
            if method['name'] == method_name:
                return method

    def get_params_from_method(self, method_name):
        """
        get all params from the method which can be set
        :param method_name: the name
        :return: an param object {name: '', default: '', count: 1, type: '', description: ''}
        """
        method = self.get_method(method_name)
        return method['keywords']['params'] if 'keywords' in method and 'params' in method['keywords'] else []

    def call_method(self, method_name, param):
        """
        calls the method with the params
        :param method_name: the name of the method to be called
        :param param: the params
        :return: Object
        """
        assert isinstance(method_name, str)
        return getattr(self, method_name)(param)

    def get_answers(self, method_name):
        """
        get all answers from the method
        :param method_name: the name of the method
        :return: a list with all answers
        """
        return self.get_method(method_name)['answers']['list']

    def get_keywords(self):
        """
        get all keywords of all methods as object
        :return: {name: '', list: [], params: []}
        """
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
        """
        get all names of all methods
        :return: list of names
        """
        all_methods = []
        for method in self.config['methods']:
            all_methods.append(method['name'])
        return all_methods
