import logging

import requests
from src.yaml.plugin import Plugin


class Trading(Plugin):
    token_required = True
    url = 'https://api.nomics.com/v1/currencies/ticker?key={key}&ids={ids}&convert=EUR&interval=1h,1d,7d'

    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)

    def make_requests(self, ids):
        logging.info(self.url.format(key=self.token, ids=ids))
        result = requests.get(self.url.format(key=self.token, ids=ids))
        print(result)
        return result

    def what_price(self, args):
        self.requiere_param(args, '$asset')
        asset = args['$asset']
        value = self.make_requests(asset)
        return {'$asset': asset, '$value': value}
