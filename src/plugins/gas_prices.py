import requests
from bs4 import BeautifulSoup, element
from src.config import config as global_config
from src.plugins.maps import Maps
from src.tools.tools import Tools
from src.yaml.plugin import Plugin


class Gas_prices(Plugin):
    def __make_request_de(self, latitude, longitude, plz, location, gas_type):
        url = "https://www.clever-tanken.de/tankstelle_liste?lat={latitude}&lon={longitude}&ort={plz}+{city}&spritsorte={sort}&r=5"
        gas_types = {'diesel': 3, 'super e5': 7, 'super e10': 5, 'erdgas': 8, 'autogas': 1, 'benzin': 5}
        url = url.format(latitude=latitude, longitude=longitude, plz=plz, city=location,
                              sort=gas_types[gas_type])
        response = requests.get(url)
        return response

    def __extract_prices(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        all_gas_stations = soup.find_all(class_='list-card-container')
        result = ''
        for station in all_gas_stations:
            assert isinstance(station, element.Tag)
            price = station.find(class_='price')
            station_name = station.find(class_='fuel-station-location-name')
            distance = station.find(class_='fuel-station-location-distance')
            assert isinstance(price, element.Tag)
            assert isinstance(station_name, element.Tag)
            assert isinstance(distance, element.Tag)
            price = str(price.contents[0].strip())
            station_name = str(station_name.contents[0])
            distance = str(distance.contents[1].contents[0])
            result += '\n**{0}** : {1} {2}'.format(price, station_name, distance)
        return result

    def get_prices(self, args):
        self.requiere_param(args, '$type')
        gas_type = args['$type']
        if global_config.env_value_exists('location'):
            location = global_config.get_env('location')
        else:
            location = 'Espelkamp'
        latitude, longitude, plz = Maps.get_coordinates(location)
        response = self.__make_request_de(latitude, longitude, plz, location, gas_type)
        result = self.__extract_prices(response)
        return {'$list': result, '$type': Tools.first_to_upper(gas_type)}

    def get_prices_in_city(self, args):
        self.requiere_param(args, '$type', '$city')
        gas_type = args['$type']
        location = args['$city']
        latitude, longitude, plz = Maps.get_coordinates(location)
        response = self.__make_request_de(latitude, longitude, plz, location, gas_type)
        result = self.__extract_prices(response)
        return {'$list': result, '$type': Tools.first_to_upper(gas_type), '$city': Tools.first_to_upper(location)}
