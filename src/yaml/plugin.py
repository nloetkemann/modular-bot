import re

from src.exceptions.not_found_exception import NotFoundException
from src.exceptions.token_exception import TokenException
from src.yaml.method import Method
import random

from src.yaml.param import AnswerParam


class Plugin:
    token_required = False
    token = ""

    def __init__(self, name, config):
        self.name = name
        self.methods = {}
        self.__config = config
        for method in config['methods']:
            call_method = self.__get_method_by_name(method['name'])
            self.methods[method['name']] = Method(method, call_method)

        if self.token_required:
            self.__require_token()

    def get_name(self):
        return self.name

    def __get_method_by_name(self, method_name):
        assert isinstance(method_name, str)
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

    def requiere_keyword_param(self, param, name):
        """
        should be called in the method of the plugin, checks if a parameter is set, which is requiered
        :param param: all params  of the method
        :param name: the name of the requiered param
        :exception: NotFoundException if the param is not set
        """
        if name not in param:
            raise NotFoundException('Parameter not found: {0}'.format(name))

    def get_all_keywords(self):
        """
        get all keywords from all methods
        :return:
        """
        keywords = []
        for method in self.methods:
            keywords.append(self.methods[method])

        return keywords

    def call_method(self, method_name, params):
        """
        calls the method by name and returns the answer of that method
        :param method_name: the name of the method
        :param params: the params for the method
        :return: a string with the answer
        """
        assert isinstance(method_name, str)
        assert isinstance(params, dict)
        answer_params = self.__get_method_by_name(method_name)(params)
        return self.__answer(method_name, answer_params)

    def __answer(self, method_name, given_params):
        """
        gets the answers from the method and checks if all params which are required are
        given in the parameter given_params
        :param method_name: the name of the method
        :param given_params: all params to be replaced in the answer
        :return: a string with the answer
        """
        assert isinstance(method_name, str)
        assert isinstance(given_params, dict)
        answers = self.methods[method_name].get_answers()
        answer_list = answers.get_list()
        required_params = answers.get_params()
        index = random.randint(0, len(answer_list) - 1)
        answer = answer_list[index]

        for param in required_params:
            assert isinstance(param, AnswerParam)
            if param.is_required() and param.get_name() not in given_params:
                raise NotFoundException('{0} in Answerparam'.format(param.get_name()))
            else:
                # param is not given, so it will be replaced with the brackets
                answer = re.sub(r'\([A-Za-z\d\s]*\${0}\b[A-Za-z\d\s]*\)\?'.format(param.get_name()[1:]), '', answer)
        for key in given_params:
            answer = answer.replace(key, given_params[key])
        return answer
