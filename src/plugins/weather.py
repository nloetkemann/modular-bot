import requests
from src.config import config
from src.exceptions.http_exception import HTTPException
from src.yaml.plugin import Plugin
from src.config import config as global_config


class Weather(Plugin):
    token_required = True
    default_location = 'Berlin'
    api_url = 'https://api.openweathermap.org/data/2.5/forecast?q={location},de&units=metric&lang={language}&appid={token}'

    def __init__(self, name, config):
        super().__init__(name, config)
        if global_config.env_value_exists('language'):
            self.language = global_config.get_env('language')
        else:
            self.language = 'de'

    def get_weather(self, args):
        if '$standort' in args:
            location = args['$standort']
        elif config.env_value_exists('location'):
            location = config.get_env('location')
        else:
            location = self.default_location
        response = {'$standort': location}
        result = self.weather_call(location)
        if '$time' in args:
            time = args['$time']
            response['$time'] = time
            temp, description = self.weather_forecast(result, time)
        else:
            temp, description = self.weather_today(result)

        response['$weather'] = description + ' mit ' + str(temp) + ' Grad'
        return response

    def weather_call(self, location):
        url = self.api_url.format(location=location, language=self.language, token=self.token)
        result, ok = self.do_request(url)
        if ok:
            return result
        raise HTTPException('Weatherplugin: ' + result)

    @staticmethod
    def do_request(url):
        r = requests.get(url)
        if r.status_code != 200:
            return r.text, False
        return r.json(), True

    @staticmethod
    def weather_today(response):
        today = response['list'][0]
        temperature = today['main']['temp']
        description = today['weather'][0]['description']
        return temperature, description

    @staticmethod
    def weather_forecast(response, date):

        def compare_tmstp(target, tmstp):
            if target - tmstp < max_diff:
                return tmstp

        max_diff = 10800
        weather_list = response['list']

        for weather in weather_list:
            if compare_tmstp(date, weather['dt']) is not None:
                return weather['main']['temp'], weather['weather'][0]['description']

        return None, None
