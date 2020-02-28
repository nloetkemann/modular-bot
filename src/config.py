# -----------------------------------------------------------
# stores the config loaded from the yaml files
#
# 2020 Nikita Lötkemann, Rahden, Germany
# email n.loetkemann@fh-bielefeld.de
# -----------------------------------------------------------
import os
import yaml

from src.exceptions.config_exception import ConfigException


class Config:
    """Stores the config loaded from the yaml files. Serves as Storage"""

    def __init__(self, config_path='./test.yaml'):
        ok, error = self.validate_config(config_path)
        if not ok:
            raise ConfigException('The Config file is not correct formatted: ' + error)
        self.config = self.__read_config_file(config_path)

        self.name = self.config['bot']['name']
        self.environment = self.config['bot']['environment']
        self.plugins = self.config['bot']['plugins']
        self.desciption = self.config['bot']['description']




    @staticmethod
    def __read_config_file(path):
        if not os.path.isfile(path):
            raise FileNotFoundError('The config file is missing.')

        with open(path, 'r') as config_file:
            return yaml.load(config_file, Loader=yaml.FullLoader)

    @staticmethod
    def validate_config(path):
        try:
            config = Config.__read_config_file(path)
        except FileNotFoundError as e:
            return False, 'File not found'

        if 'bot' in config:
            bot_config = config['bot']
            if 'name' not in bot_config:
                return False, 'name not found'
            elif 'environment' not in bot_config:
                return False, 'environment not found'
            elif 'plugins' not in bot_config:
                return False, 'plugins not found'

            if not isinstance(bot_config['name'], str):
                return False, 'name is not a string'
            elif not isinstance(bot_config['environment'], list):
                return False, 'environment is not a list'
            elif not isinstance(bot_config['plugins'], list):
                return False, 'plugins is not a list'
            return True, ''
        else:
            return False, 'bot'

