import wolframalpha
from src.config import config as global_config
from src.yaml.plugin import Plugin


class Wolfram(Plugin):
    token_required = True

    def __init__(self, name, config):
        super().__init__(name, config)
        self.wolfram_client = wolframalpha.Client(global_config.secrets.get_secret('wolfram'))

    def add_numbers(self, args):
        self.requiere_param(args, '$first', '$second')
        result = self.wolfram_client.query('{0}+{1}'.format(args['$first'], args['$second']))
        value = next(result.results).text
        return {'$result': value}
