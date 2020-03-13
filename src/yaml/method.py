from src.yaml.attribute import Keyword, Answer


class Method:
    """
    class for a method of the yaml file
    """
    def __init__(self, config, method):
        self.name = config['name']
        self.keywords = Keyword(config['keywords'])
        self.answers = Answer(config['answers'])
        self.method = method
        self.help = config['help'] if 'help' in config else ''

    def get_name(self):
        return self.name

    def get_help(self):
        return self.help

    def get_keywords(self):
        return self.keywords

    def get_answers(self):
        return self.answers

    def call_method(self, params):
        return self.method(params)
