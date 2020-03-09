from src.yaml.param import KeywordParam, AnswerParam


class Attribute:
    """
    Abstract class for the Attributes
    """

    def __init__(self, config):
        self.list = []
        self.params = {}
        for entry in config['list']:
            self.list.append(entry)

    def get_list(self):
        return self.list

    def get_params(self):
        return self.params.values()


class Keyword(Attribute):
    """
    class for the keyword attribute of the yaml
    """

    def __init__(self, config):
        super().__init__(config)
        if 'params' in config:
            for entry in config['params']:
                self.params[entry['name']] = KeywordParam(entry)

    def get_count_of_param(self, param_name):
        param = self.params[param_name]
        return param.get_count()

    def get_type_of_param(self, param_name):
        param = self.params[param_name]
        return param.get_type()


class Answer(Attribute):
    """
    class for the keyword attribute of the yaml
    """

    def __init__(self, config):
        super().__init__(config)
        if 'params' in config:
            for entry in config['params']:
                self.params[entry['name']] = AnswerParam(entry)
