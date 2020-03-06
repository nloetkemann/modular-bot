from src.tools import Tools


class Secrets:
    def __init__(self, path: str):
        Tools.validate_yaml('./schemas/secrets-schema.yaml', path)
        self.secrets = Tools.read_config_file(path)['secrets']

    def get_secret(self, name: str, parent: str = 'plugin'):
        return self.secrets[parent][name]
