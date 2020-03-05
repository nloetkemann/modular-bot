import datetime
from src.config import config
from src.yaml.plugin import Plugin


class Weather(Plugin):
    token_required = True
    default_location = 'Berlin'

    def get_weather(self, args):
        if '$standort' in args:
            location = args['$standort']
        elif config.env_value_exists('location'):
            location = config.get_env('location')
        else:
            location = self.default_location
        if '$time' in args:
            time = args['$time']
        else:
            time = datetime.datetime.now()

        print(location, time)
