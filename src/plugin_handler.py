import logging
import re
from src.exceptions.too_many_words_exception import TooManyWordsException
from src.exceptions.not_found_exception import NotFoundException
from src.tools.tools import Tools
from src.yaml.method import Method
from src.yaml.param import KeywordParam

logger = logging.getLogger(__name__)


class PluginHandler:
    """:keywords all keywords of all plugins and their methods. Format: {'PluginName': {'method_name': ['keyword']}}"""
    keywords = {}

    def __init__(self, all_plugins):
        assert isinstance(all_plugins, list)
        self.all_plugins = all_plugins

        for plugin in all_plugins:
            logger.info('Activate Plugins: {0}'.format(plugin.get_name()))
            methods = plugin.get_all_keywords()
            plugin_method = {}
            for method in methods:
                assert isinstance(method, Method)
                keywords = method.get_keywords()
                list_methods = self.__get_keywords_as_regex(keywords.get_list(), keywords.get_params())
                plugin_method[method.get_name()] = list_methods
            self.keywords[plugin.get_name()] = plugin_method

    def get_plugin_by_name(self, plugin_name):
        """
        gets the plugin by name
        :param plugin_name: name of the plugin
        :return: the Plugin
        """
        for plugin in self.all_plugins:
            if plugin.get_name() == plugin_name:
                return plugin

    def _get_regex_for_variable_type(self, param_type: str, count: int):
        if param_type == 'integer':
            if count > 1:
                return r'(\d *){1,' + str(count - 1) + r'}\d'
            else:
                return r'\d+'
        elif param_type == 'number':
            if count > 1:
                return r'(\d+\.?\d? *){1,' + str(count - 1) + r'}\d+\.?\d?'
            else:
                return r'\d+\.?\d?'
        else:
            if count > 1:
                return r'[A-Za-z\d]+( [A-Za-z\d]+){0,' + str(count - 1) + r'}'
            else:
                return r'[A-Za-z\d]+'

    def __get_keywords_as_regex(self, keywords, params):
        """
        converts the given regex from the yaml files to valid regex, replacing the params with regex
        :param keywords: the keyword list from the yaml file
        :param params: the keyword params from the yaml file
        :return: for each method an array with the regex keywords (Format: [(regex, matching keyword from yaml file), ...])
        """
        regex_matcher = []
        for keyword in keywords:
            match = keyword
            if len(params) > 0:
                for param in params:
                    assert isinstance(param, KeywordParam)
                    if param.get_name() in keyword:
                        reg_param = self._get_regex_for_variable_type(param.get_type(), param.get_count())
                        match = match.replace(param.get_name(), reg_param)
            regex_matcher.append((match, keyword))
        return regex_matcher

    def validate_user_input(self, user_input):
        """
        validates the user_input, means iterates through the plugins and checks with the given regex. which plugin,
        which method and which parameter are given
        :param user_input: the user input
        :return: [] an array of three elems. first the plugin, second the method, third the param found
        """
        assert isinstance(user_input, str)
        for key in self.keywords:
            for method in self.keywords[key]:
                for match in self.keywords[key][method]:
                    if re.match(match[0], user_input):
                        method_object = self.get_plugin_by_name(key).get_method_attr(method)
                        foundparams = self.__get_param_from_user_input(match[1], user_input, method_object)
                        # self.__too_many_params(key, method, foundparams)
                        logger.info('Plugin {0} found with method {1} params: {2}'.format(key, method, str(foundparams)))
                        return self.get_plugin_by_name(key), method, foundparams
        raise NotFoundException('No Plugin or no Method found for "{0}"'.format(user_input))

    def __too_many_params(self, plugin, method, params):
        plugin = self.get_plugin_by_name(plugin)
        method = plugin.get_method_attr(method)
        for param_name in params:
            count = method.get_keywords().get_count_of_param(param_name[1:])
            words = params[param_name].split(' ')
            if count < len(words):
                raise TooManyWordsException(
                    '{0} given with a length of {1}, allowed is {2}'.format(params[param_name], len(words),
                                                                            count))

    def __get_param_from_user_input(self, original, user_input,
                                    method):  # todo abhaenig machen von dem regex aus der yaml!!!!!
        """
        iterates through all params and extracts the params from the user_input
        :param original: the value given in the plugin yaml file. Containing parameters starting with $
        :param user_input: the user input
        :return object of the params. Format: {$param: 'value', ...}
        """
        params = re.findall(r'\$[A-Za-z]+', original)
        foundparams = {}
        for param in params:
            count = method.get_keywords().get_count_of_param(param[1:])
            param_type = method.get_keywords().get_type_of_param(param[1:])
            foundparam = self.__trim_words(user_input, original.replace(param, '', 1), count, param_type)
            if foundparam is not None and foundparam != '':
                foundparams[param] = foundparam
                user_input = user_input.replace(foundparam, '', 1)
        return foundparams

    def __trim_words(self, user_input, regex, count, param_type):
        """
        first remove all words which are the same from regex and the user input
        then invert the match and replace the result in the user input
        :param user_input: the user input
        :param regex: the regex without the parameter (without $param)
        :return: the found param
        """
        regex = Tools.remove_regex(regex)
        regex_words = regex.split(' ')
        for word in user_input.split(' '):
            if word in regex_words:
                user_input = re.sub(word, '', user_input, 1)

        invert = r'((?!{0}).)*'
        param_regex = self._get_regex_for_variable_type(param_type, count)
        found = re.sub(invert.format(param_regex), '', user_input, 1)
        found = found.split(' ')[0:count]
        return ' '.join(found)
