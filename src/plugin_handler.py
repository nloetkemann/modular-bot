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
                        print(match[0])
                        plugin = self.get_plugin_by_name(key)
                        method = plugin.get_method_attr(method).get_keywords()
                        count = method.get_count_of_param(match)
                        type = method.get_type_of_param(match)

                        print(count, type)
                        foundparams = self.__get_param_from_user_input(match[1], user_input, type, count)
                        print(foundparams)
                        print(key, method)
                        self.__too_many_params(key, method, foundparams)
                        logger.info('Plugin found with params: {0}'.format(str(foundparams)))
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

    def __get_param_from_user_input(self, original, user_input, param_type,
                                    count):  # todo abhaenig machen von dem regex aus der yaml!!!!!
        """
        iterates through all params and extracts the params from the user_input
        :param original: the value given in the plugin yaml file. Containing parameters starting with $
        :param user_input: the user input
        :return object of the params. Format: {$param: 'value', ...}
        """
        params = re.findall(r'\$[A-Za-z]+', original)
        foundparams = {}
        for param in params:
            foundparam = self.__trim_words(user_input, original.replace(param, '', 1), param_type, count)
            if foundparam is not None and foundparam != '':
                foundparams[param] = foundparam
                user_input = user_input.replace(foundparam, '')
        return foundparams

    def _get_regex_for_variable_type(self, param_type, count):
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

    def __trim_words(self, userinput, regex, param_type, count):
        """
        iterates through every word from the user_input und compares it with the regex
        if its the same, delete it, if not, its a parameter
        :param userinput: the user input
        :param regex: the regex without the parameter (without $param)
        :return: the found param
        """
        regex = Tools.remove_regex(regex)
        counter, flag = 0, 0
        regex_words = regex.split(' ')
        for word in userinput.split(' '):
            for reword in range(counter, len(regex_words), 1):
                if word == regex_words[reword]:
                    userinput = userinput.replace(word, '', 1).strip()
                    counter += 1
                    if flag == 1:
                        flag = 2
                    break
                elif word != regex_words[reword] and flag == 0 and word != '':
                    flag = 1
                elif word != regex_words[reword] and flag == 2 and word != '':
                    userinput = userinput.replace(word, '', 1).strip()
        param_regex = self._get_regex_for_variable_type(param_type, count)
        if re.match(param_regex, userinput):
            return userinput
        else:
            return ''


    def test(self):
        regex = r'was ist \d+\.?\d? \+ \d+\.?\d?'
        param_text = r'was ist $first \\+ $second'

        user_input = 'was ist 2 + 2'

        type = 'number'
        count = 1

        number_regex = r'\d+\.?\d?'

        invert = r'((?!{0}).)*'

        print(re.match(invert.format(number_regex), user_input))