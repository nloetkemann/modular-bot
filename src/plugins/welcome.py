from src.yaml.plugin import Plugin
from src.config import config


class Welcome(Plugin):

    def say_hello(self, args):
        return {}

    def how_are_you(self, args):
        return {}

    def who_are_you(self, args):
        return {'$name': config.name}

    def what_are_you_doing(self, args):
        return  {'$doing': 'Gar nichts', '$how': 'und das sehr langsam'}
