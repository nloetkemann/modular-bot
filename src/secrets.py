from src.tools import Tools


class Secrets:
    def __init__(self, path: str):
        Tools.validate_yaml('./schemas/secrets-schema.yaml', path)
        self.secrets = Tools.read_config_file(path)['secrets']
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

    def get_secret(self, name: str, parent: str = 'plugins'):
        name = name.lower()
        if parent in self.secrets and name in self.secrets[parent]:
            return self.secrets[parent][name]
        return ''
