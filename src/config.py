# -----------------------------------------------------------
# stores the config loaded from the yaml files
#
# 2020 Nikita Lötkemann, Rahden, Germany
# email n.loetkemann@fh-bielefeld.de
# -----------------------------------------------------------
import os
import re
from src.bot.discord_bot import DiscordBot
from src.bot.slack_bot import SlackBot
from src.bot.telegram_bot import TelegramBot
from src.exceptions.config_exception import ConfigException
from src.exceptions.not_found_exception import NotFoundException
from src.secrets import Secrets
from src.tools.tools import Tools


class Config:
    """Stores the config loaded from the yaml files. Serves as Storage"""
    config = None
    name = ''
    environment = []
    plugins = []
    description = ''
    list_plugin_objects = []
    bots = {}

    messenger_names = {'': ''}

    def __init__(self, config_path='./config.yaml', secrets_path='', translation_dir='./translation'):
        self.translation_dir = translation_dir
        self.secrets = Secrets(secrets_path)
        self.load_from_file(config_path)

    def load_from_file(self, config_path: str):
        ok, error = Tools.validate_yaml('./schemas/config-schema.yaml', config_path)
        if not ok:
            raise ConfigException('The Config file is not correct formatted: ' + error)
        self.config = Tools.read_config_file(config_path)

        self.name = self.config['bot']['name'] if 'BOT_NAME' not in os.environ else os.environ['BOT_NAME']
        self.environment = self.config['bot']['environment']
        self.__extract_env_variables_from_env()
        self.plugins = self.config['bot']['plugins']
        self.description = self.config['bot']['description'] if 'BOT_DESCRIPTION' not in os.environ else os.environ[
            'BOT_DESCRIPTION']

        self.list_plugin_objects = []

        self.bots = {}
        for bot_name in self.config['bot']['messenger']:
            bot = self.__create_bot_by_name(bot_name)
            self.bots[bot_name] = bot

    def __extract_env_variables_from_env(self):
        for var in os.environ:
            if re.match(r'^(ENV_).*', var):
                key = re.sub(r'^(ENV_)', '', var).lower()
                self.environment.append({'name': key, 'value': os.environ[var]})

    def __create_bot_by_name(self, bot_name: str):
        token = self.secrets.get_secret(bot_name, 'bots')
        if bot_name == 'telegram':
            bot = TelegramBot(token)
        elif bot_name == 'discord':
            bot = DiscordBot(token)
        elif bot_name == 'slack':
            bot = SlackBot(token)
        else:
            raise NotFoundException('{0} does not exist'.format(bot_name))
        return bot

    def add_to_plugins(self, plugin):
        self.list_plugin_objects.append(plugin)

    def get_plugins(self) -> list:
        return self.list_plugin_objects

    def get_env(self, name: str) -> str:
        """
        returns the value of the environment variable
        :param name: the name of the variable
        :return: the value
        """
        for entry in self.environment:
            if 'name' in entry and entry['name'] == name:
                return entry['value']
        return ''

    def env_value_exists(self, name: str) -> bool:
        """
        checks if the environment variable is set
        :param name: the name of the variable
        :return: if set or not
        """
        for entry in self.environment:
            if 'name' in entry and entry['name'] == name:
                return True
        return False


config = Config(secrets_path='./secrets.yaml')
