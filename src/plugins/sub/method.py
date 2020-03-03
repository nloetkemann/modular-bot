from src.plugins.sub.attribute import Keyword, Answer


class Method:
    def __init__(self, config, method):
        self.name = config['name']
        self.keywords = Keyword(config['keywords'])
        self.answers = Answer(config['answers'])
        self.method = method
