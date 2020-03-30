import os

from src.tools.tools import Tools


class Secrets:
    secrets = {}
    bot_envs_names = {'slack': 'BOT_SLACK', 'telegram': 'BOT_TELEGRAM', 'discord': 'BOT_DISCORD'}
    plugin_env_names = {'wolfram': 'WOLFRAM_ENV', 'weather': 'WEATHER_ENV'}
    env_names = {}

    def __init__(self, path: str = ""):
        if path != "":
            self.load_from_file(path)
        else:
            self.load_from_env()

    def load_from_env(self):
        for bot in self.bot_envs_names:
            if self.bot_envs_names[bot] in os.environ:
                self.secrets[bot] = os.environ[self.bot_envs_names[bot]]

        for plugin in self.plugin_env_names:
            if self.plugin_env_names[plugin] in os.environ:
                self.secrets[plugin] = os.environ[self.plugin_env_names[plugin]]

        for env in self.env_names:
            if self.env_names[env] in os.environ:
                self.secrets[env] = os.environ[self.env_names[env]]

    def load_from_file(self, path: str):
        try:
            Tools.validate_yaml('./schemas/secrets-schema.yaml', path)
            self.secrets = Tools.read_config_file(path)['secrets']
        except TypeError:
            self.secrets = {}
            return
        plugins = {}
        bots = {}
        environment = {}
        for plugin in self.secrets['plugins']:
            for item in plugin:
                plugins[item] = plugin[item]
        for bot in self.secrets['bots']:
            for item in bot:
                bots[item] = bot[item]
        for value in self.secrets['environment']:
            for item in value:
                environment[item] = value[item]
        self.secrets = {'plugins': plugins, 'bots': bots, 'environment': environment}

    def get_secret(self, name: str, parent: str = 'plugins') -> str:
        name = name.lower()
        if parent in self.secrets and name in self.secrets[parent]:
            return self.secrets[parent][name]
        return ''
