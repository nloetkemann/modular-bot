# -----------------------------------------------------------
# stores the config loaded from the yaml files
#
# 2020 Nikita Lötkemann, Rahden, Germany
# email n.loetkemann@fh-bielefeld.de
# -----------------------------------------------------------
import os
import yaml
import yamale

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
        """
        reads the config file and returns it
        :param path: the path of the config file
        :return: the configuration
        """
        if not os.path.isfile(path):
            raise FileNotFoundError('The config file is missing.')

        with open(path, 'r') as config_file:
            return yaml.load(config_file)

    @staticmethod
    def validate_config(path):
        """
        checks if the yaml config file is valid
        :param path: the path of the config file
        :return: bool, ''
        """
        schema = yamale.make_schema('./schemas/config-schema.yaml')
        data = yamale.make_data(path)
        try:
            yamale.validate(schema, data)
        except ValueError as e:
            print(e)
            return False, 'Yaml file is mal formated. ' + str(e)
        return True, ''

    def get_env(self, name):
        """
        returns the value of the environment variable
        :param name: the name of the variable
        :return: the value
        """
        for entry in self.environment:
            print(entry)
            if 'name' in entry and entry['name'] == name:
                return entry['value']
        return ''

    def env_value_exists(self, name):
        """
        checks if the environment variable is set
        :param name: the name of the variable
        :return: if set or not
        """
        for entry in self.environment:
            if 'name' in entry and entry['name'] == name:
                return True
        return False


config = Config()
