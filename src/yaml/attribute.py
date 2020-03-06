from src.yaml.param import KeywordParam, AnswerParam


class Attribute:
    """
    Abstract class for the Attributes
    """
    def __init__(self, config):
        self.list = []
        self.params = []
        for entry in config['list']:
            self.list.append(entry)

    def get_list(self):
        return self.list

    def get_params(self):
        return self.params


class Keyword(Attribute):
    """
    class for the keyword attribute of the yaml
    """
    def __init__(self, config):
        super().__init__(config)
        if 'params' in config:
            for entry in config['params']:
                self.params.append(KeywordParam(entry))


class Answer(Attribute):
    """
    class for the keyword attribute of the yaml
    """
    def __init__(self, config):
        super().__init__(config)
        if 'params' in config:
            for entry in config['params']:
                self.params.append(AnswerParam(entry))
