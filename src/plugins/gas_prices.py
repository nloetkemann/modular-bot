import requests
from bs4 import BeautifulSoup

from src.plugins.maps import Maps
from src.yaml.plugin import Plugin


class Gas_prices(Plugin):
    url = "https://www.clever-tanken.de/tankstelle_liste?lat={latitude}&lon={longitude}&ort={plz}+{city}&spritsorte={sort}&r=5"
    gas_types = {'diesel': 3, 'super e5': 7, 'super e10': 5, 'erdgas': 8, 'autogas': 1}

    def get_prices(self, args):
        self.requiere_param(args, '$type')
        gas_type = args['$type']
        latitude, longitude = Maps.get_coordinates('Espelkamp')
        url = self.url.format(latitude=latitude, longitude=longitude, plz='32339', city='Espelkamp',
                              sort=self.gas_types[gas_type])
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        return {'$price': '1.10€', '$type': 'Diesel'}
