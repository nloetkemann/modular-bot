from src.exceptions.token_exception import TokenException
from src.plugins.plugin import Plugin


class Weather(Plugin):
    token_required = True

    def __init__(self, name, config):
        super().__init__(name, config)

    def get_weather(self, args):
        print(args)
        print("weather")
