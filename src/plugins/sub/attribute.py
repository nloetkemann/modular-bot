from src.plugins.sub.param import KeywordParam, AnswerParam


class Attribute:
    def __init__(self, config):
        self.list = []
        self.params = []
        for entry in config['list']:
            self.list.append(entry)


class Keyword(Attribute):
    def __init__(self, config):
        super().__init__(config)
        for entry in config['params']:
            self.params.append(KeywordParam(entry))


class Answer(Attribute):
    def __init__(self, config):
        super().__init__(config)
        for entry in config['params']:
            self.params.append(AnswerParam(entry))
