from src.exceptions.not_found_exception import NotFoundException
from src.exceptions.token_exception import TokenException
from src.plugins.sub.method import Method


class Plugin:
    token_required = False
    token = ""

    def __init__(self, name, config):
        self.name = name
        self.methods = []
        self.__config = config
        for method in config['methods']:
            self.methods.append(Method(config, self.__get_method_by_name(method['name'])))

        if self.token_required:
            self.__require_token()

    def __get_method_by_name(self, method_name):
        return getattr(self, method_name)

    def __require_token(self):
        """
        should be called if a token is required
        this will be checked when calling the constuctor of the plugin
        :exception: TokenException if no token is set
        """
        if 'token' in self.__config and self.__config['token'] != '':
            self.token = self.__config['token']
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
