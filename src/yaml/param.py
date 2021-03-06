class Param:
    """
    Abstract class for all params
    """

    def __init__(self, config):
        self.name = config['name']
        self.description = config['description'] if 'description' in config else ''
        self.__value = ''

    def get_name(self):
        return '$' + self.name

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value


class KeywordParam(Param):
    """
    class for the keyword param
    """
    def __init__(self, config):
        super().__init__(config)
        self.count = config['count'] if 'count' in config else 1
        self.type = config['type'] if 'type' in config else 'string'

    def get_type(self):
        return self.type

    def get_count(self):
        return self.count


class AnswerParam(Param):
    """
    class for the answer param
    """
    def __init__(self, config):
        super().__init__(config)
        self.required = True if 'required' not in config else config['required']

    def is_required(self):
        return self.required
