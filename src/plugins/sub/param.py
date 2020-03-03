class Param:
    def __init__(self, config):
        self.name = config['name']
        self.description = config['description']
        self.__value = ''

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value


class KeywordParam(Param):
    def __init__(self, config):
        super().__init__(config)
        self.count = config['count'] if 'count' in config else 1
        self.type = config['type'] if 'type' in config else 'string'


class AnswerParam(Param):
    pass
