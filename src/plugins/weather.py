from src.plugins.plugin import Plugin


class Weather(Plugin):
    token_required = True

    def get_weather(self, args):
        print(args)
        print("weather")
