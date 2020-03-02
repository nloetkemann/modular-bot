import re


class PluginHandler:
    """:keywords all keywords of all plugins and their methods. Format: {'PluginName': {'method_name': ['keyword']}}"""
    keywords = {}

    def __init__(self, all_plugins):
        assert isinstance(all_plugins, list)
        self.all_plugins = all_plugins
        for plugin in all_plugins:
            keywords = plugin.get_keywords()
            plugin_method = {}
            for keyword in keywords:
                list_keywords = self.__get_keywords_as_regex(keyword['list'], keyword['params'])
                plugin_method[keyword['name']] = list_keywords
            self.keywords[plugin.get_name()] = plugin_method

    def __get_keywords_as_regex(self, keywords, params):
        regex_matcher = []
        for keyword in keywords:
            match = keyword
            if len(params) > 0:
                for param in params:
                    if param['name'] in keyword:
                        if 'type' in param and param['type'] == 'integer':
                            if 'count' in param and param['count'] > 1:
                                count = param['count']
                                match = match.replace('$' + param['name'], r'(\d *){1,' + str(count - 1) + r'}\d')
                            else:
                                match = match.replace('$' + param['name'], r'\d+')
                        else:
                            if 'count' in param and param['count'] > 1:
                                count = param['count']
                                match = match.replace('$' + param['name'],
                                                      r'[A-Za-z\d]+( [A-Za-z\d]+){0,' + str(count - 1) + r'}')
                            else:
                                match = match.replace('$' + param['name'], r'[A-Za-z\d]+')
            regex_matcher.append((match, keyword))
        return regex_matcher

    def validate_user_input(self, user_input):
        assert isinstance(user_input, str)
        for key in self.keywords:
            for method in self.keywords[key]:
                for match in self.keywords[key][method]:
                    if re.match(match[0], user_input):
                        foundparams = self.__get_param_from_user_input(match[1], user_input)
                        return key, method, foundparams

    def __get_param_from_user_input(self, original, user_input):
        params = re.findall(r'\$[A-Za-z]+', original)
        foundparams = {}
        for param in params:
            foundparam = self.__trim_words(user_input, original.replace(param, '', 1))
            if foundparam is not None:
                foundparams[param] = foundparam
            if foundparam != '':
                user_input = user_input.replace(foundparam, '')

        return foundparams

    def __trim_words(self, userinput, regex):
        regex = self.__trim_regex_letters(regex)
        print(userinput, regex)
        counter = 0
        flag = ''
        found = ''
        regex_words = regex.split(' ')
        for word in userinput.split(' '):
            for reword in range(counter, len(regex_words), 1):
                if word == regex_words[reword]:
                    userinput = userinput.replace(word, '').strip()
                    counter += 1
                    if flag == 'blub':
                        flag = 'done'
                    break
                elif word != regex_words[reword] and flag == '':
                    flag = 'blub'
                    found += ' ' + word
                elif word != regex_words[reword] and flag == 'blub':
                    found += ' ' + word
                elif word != regex_words[reword] and flag == 'done':
                    userinput = userinput.replace(word, '').strip()

        print(userinput)
        return userinput

    def __trim_regex_letters(self, regex):
        return re.sub(r'(\(|\))+', '', regex)
