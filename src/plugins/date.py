import datetime
from src.config import config as global_config
from src.exceptions.wrong_name_exception import WrongNameException
from src.yaml.plugin import Plugin


class Date(Plugin):
    day_names = {
        'de': ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'],
        'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }

    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)
        if global_config.env_value_exists('language'):
            self.language = global_config.get_env('language')

    def __get_day_name(self, day):
        try:
            return self.day_names[self.language][day]
        except IndexError:
            raise WrongNameException('There is no day {0} in this language: {1}'.format(day, self.language))

    @staticmethod
    def __add_zero_if_required(value: int):
        if value <= 9:
            return '0' + str(value)
        return str(value)

    def get_time(self, args):
        date = datetime.datetime.now()
        hour = self.__add_zero_if_required(date.hour)
        minute = self.__add_zero_if_required(date.minute)
        return {'$time': '{0}:{1}'.format(hour, minute)}

    def get_date(self, args):
        date = datetime.datetime.now()
        day = self.__get_day_name(date.weekday())
        return {'$day': day, '$date': '{0}.{1}'.format(date.day, date.month)}
