from src.plugins.plugin import Plugin


class Weather(Plugin):

    def get_weather(self, args):
        print(args)
        print("weather")
