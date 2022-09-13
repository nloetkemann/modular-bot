import re

from src.config import config
from src.exceptions.not_found_exception import NotFoundException
from src.exceptions.token_exception import TokenException
from src.tools.tools import Tools
from src.translation import Translation
from src.yaml.method import Method
import random

from src.yaml.param import AnswerParam


class Plugin:
    token_required = False
    token = ""

    def __init__(self, name, plugin_config):
        self.name = name
        self.methods = {}
        self.translation = Translation(self.name, f'./plugins/{self.name.lower()}/translation.yaml')
        self.__config = plugin_config
        self.__load_translation()

        for method in plugin_config['methods']:
            call_method = self.__get_method_by_name(method['name'])
            self.methods[method['name']] = Method(method, call_method)

        if self.token_required:
            self.__require_token()

        config.add_to_plugins(self)

    def __load_translation(self):
        language = config.language
        description_key = self.__config['description']
        self.__config['description'] = self.translation.get_other_translation(description_key, language)

        methods = []
        for method in self.__config['methods']:
            # for help
            if 'help' in method:
                translation = self.translation.get_other_translation(method['help'], language)
                if translation != "":
                    method['help'] = translation

            # for keywords params
            if 'params' in method['keywords']:
                params = []
                for param in method['keywords']['params']:
                    translation = self.translation.get_other_translation(param['description'], language)
                    if translation != "":
                        param['description'] = translation
                        params.append(param)
                method['keywords']['params'] = params

            # for answers params
            if 'params' in method['answers']:
                params = []
                for param in method['answers']['params']:
                    translation = self.translation.get_other_translation(param['description'], language)
                    param['description'] = translation
                    params.append(param)
                method['answers']['params'] = params

            # for keywords
            if 'list' in method['keywords']:
                key_word_list = []
                for keyword in method['keywords']['list']:
                    translation = self.translation.get_keyword_translation(keyword, language)
                    if translation != "":
                        key_word_list.append(translation)
                method['keywords']['list'] = key_word_list

            # for answers
            if 'list' in method['answers']:
                answer_list = []
                for answer in method['answers']['list']:
                    translation = self.translation.get_answer_translation(answer, language)
                    if translation != "":
                        answer_list.append(translation)
                method['answers']['list'] = answer_list
            methods.append(method)

        self.__config['methods'] = methods

    def get_name(self):
        return self.name

    def get_description(self):
        return self.__config['description'] if 'description' in self.__config else ''

    def get_method_attr(self, method_name):
        return self.methods[method_name]

    def __get_method_by_name(self, method_name):
        assert isinstance(method_name, str)
        return getattr(self, method_name)

    def __require_token(self):
        """
        should be called if a token is required
        this will be checked when calling the constuctor of the plugin
        :exception: TokenException if no token is set
        """
        token = config.secrets.get_secret(self.name)
        if token is not '':
            self.token = token
        else:
            raise TokenException(self.__class__)

    def requiere_param(self, param, *args):
        """
        should be called in the method of the plugin, checks if a parameter is set, which is requiered
        :param param: all params  of the method
        :param name: the name of the requiered param
        :exception: NotFoundException if the param is not set
        """
        for name in args:
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
        if '__photo' in answer_params:
            return self.__answer(method_name, answer_params), answer_params['__photo'], 'photo'
        elif '__file' in answer_params:
            return self.__answer(method_name, answer_params), answer_params['__file'], 'file'
        return self.__answer(method_name, answer_params), None, ''

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
        answer = Tools.remove_regex(answer)

        for param in required_params:
            assert isinstance(param, AnswerParam)
            if param.is_required() and param.get_name() not in given_params:
                raise NotFoundException('{0} in Answerparam'.format(param.get_name()))
            elif param.get_name() not in given_params:
                # param is not given, so it will be replaced with the brackets
                answer = re.sub(r'\([A-Za-z\d\s]*\${0}\b[A-Za-z\d\s]*\)\?'.format(param.get_name()[1:]), '', answer)
        for key in given_params:
            answer = answer.replace(key, str(given_params[key]))
        return answer
