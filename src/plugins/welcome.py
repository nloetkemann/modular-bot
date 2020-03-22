import datetime

from src.yaml.plugin import Plugin
from src.config import config


class Welcome(Plugin):
    born_date = datetime.datetime(2020, 2, 28)

    def say_hello(self, args):
        return {}

    def how_are_you(self, args):
        return {}

    def who_are_you(self, args):
        return {'$name': config.name}

    def what_are_you_doing(self, args):
        return {'$doing': 'Gar nichts', '$how': 'und das sehr langsam'}

    def if_bot_needs_help(self, args):
        return {}

    def how_old_is_bot(self, args):
        now = datetime.datetime.now()
        days = now - self.born_date
        return {'$days': days.days}

    def what_bot_is_able_to(self, args):
        return {}

    def where_is_your_work(self, args):
        return {}

    def what_is_your_gender(self, args):
        return {}
